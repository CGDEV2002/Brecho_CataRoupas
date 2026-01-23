from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.urls import reverse
import json
import urllib.parse
from loja.models import Produto
from .models import CarrinhoItem


def get_or_create_session_key(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


def adicionar_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id, disponivel=True)
    session_key = get_or_create_session_key(request)

    carrinho_item, created = CarrinhoItem.objects.get_or_create(
        session_key=session_key, produto=produto, defaults={"quantidade": 1}
    )

    if not created:
        carrinho_item.quantidade += 1
        carrinho_item.save()

    messages.success(request, f"{produto.nome} adicionado ao carrinho!")

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse(
            {
                "success": True,
                "message": f"{produto.nome} adicionado ao carrinho!",
                "carrinho_count": CarrinhoItem.objects.filter(
                    session_key=session_key
                ).count(),
            }
        )

    return redirect("carrinho:ver_carrinho")


def ver_carrinho(request):
    session_key = get_or_create_session_key(request)
    itens = CarrinhoItem.objects.filter(session_key=session_key)

    total = sum(item.subtotal for item in itens)

    context = {
        "itens": itens,
        "total": total,
    }
    return render(request, "carrinho/ver_carrinho.html", context)


def atualizar_quantidade(request, item_id):
    if request.method == "POST":
        session_key = get_or_create_session_key(request)
        item = get_object_or_404(CarrinhoItem, id=item_id, session_key=session_key)
        quantidade = int(request.POST.get("quantidade", 1))

        if quantidade > 0:
            item.quantidade = quantidade
            item.save()
        else:
            item.delete()

    return redirect("carrinho:ver_carrinho")


def remover_item(request, item_id):
    session_key = get_or_create_session_key(request)
    item = get_object_or_404(CarrinhoItem, id=item_id, session_key=session_key)
    item.delete()
    messages.success(request, "Item removido do carrinho!")
    return redirect("carrinho:ver_carrinho")


def finalizar_compra(request):
    session_key = get_or_create_session_key(request)
    itens = CarrinhoItem.objects.filter(session_key=session_key)

    if not itens:
        messages.error(request, "Seu carrinho está vazio!")
        return redirect("carrinho:ver_carrinho")

    if request.method == "POST":
        # Coletar dados do cliente
        nome = request.POST.get("nome")
        telefone = request.POST.get("telefone")
        endereco = request.POST.get("endereco")

        # Criar JSON do pedido
        pedido_data = {
            "cliente": {"nome": nome, "telefone": telefone, "endereco": endereco},
            "itens": [],
            "total": 0,
        }

        total = 0
        for item in itens:
            pedido_data["itens"].append(
                {
                    "produto": item.produto.nome,
                    "quantidade": item.quantidade,
                    "preco_unitario": float(item.produto.preco),
                    "subtotal": float(item.subtotal),
                }
            )
            total += item.subtotal

        pedido_data["total"] = float(total)

        # Formatar mensagem para WhatsApp
        mensagem = f"👋 *Olá! Temos um novo pedido do Brechó Online!*\n\n"
        mensagem += f"🛍️ *DETALHES DO PEDIDO*\n"
        mensagem += f"━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        mensagem += f"👤 *Cliente:* {nome}\n"
        mensagem += f"📱 *Telefone:* {telefone}\n"
        mensagem += f"📍 *Endereço de Entrega:*\n{endereco}\n\n"
        mensagem += f"📦 *PRODUTOS SELECIONADOS:*\n"
        mensagem += f"━━━━━━━━━━━━━━━━━━━━━━━━━\n"

        for item in pedido_data["itens"]:
            subtotal = item["subtotal"]
            mensagem += f"▪️ *{item['produto']}*\n"
            mensagem += f"   Quantidade: {item['quantidade']}x\n"
            mensagem += f"   Valor unitário: R$ {item['preco_unitario']:.2f}\n"
            mensagem += f"   Subtotal: R$ {subtotal:.2f}\n\n"

        mensagem += f"━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        mensagem += f"💰 *VALOR TOTAL: R$ {total:.2f}*\n\n"
        mensagem += (
            f"📞 *Entre em contato para confirmar o pedido e combinar a entrega!*\n"
        )
        mensagem += f"Obrigado pela preferência! ✨"

        numero_whatsapp = "5551996235293"

        # URL do WhatsApp
        whatsapp_url = (
            f"https://wa.me/{numero_whatsapp}?text={urllib.parse.quote(mensagem)}"
        )

        # Limpar carrinho
        itens.delete()

        return redirect(whatsapp_url)

    total = sum(item.subtotal for item in itens)

    context = {
        "itens": itens,
        "total": total,
    }
    return render(request, "carrinho/finalizar_compra.html", context)


def carrinho_count(request):
    session_key = get_or_create_session_key(request)
    count = CarrinhoItem.objects.filter(session_key=session_key).count()
    return JsonResponse({"count": count})
