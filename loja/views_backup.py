from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Produto, Categoria
from .forms import ProdutoForm, CategoriaForm, ProdutoImagemFormSet


class LojaView(ListView):
    model = Produto
    template_name = "loja/index.html"
    context_object_name = "produtos"
    paginate_by = 12

    def get_queryset(self):
        queryset = Produto.objects.filter(disponivel=True)
        categoria_slug = self.request.GET.get("categoria")
        busca = self.request.GET.get("q")

        if categoria_slug:
            categoria = get_object_or_404(Categoria, slug=categoria_slug)
            queryset = queryset.filter(categoria=categoria)

        if busca:
            queryset = queryset.filter(nome__icontains=busca)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categorias"] = Categoria.objects.all()
        context["categoria_selecionada"] = self.request.GET.get("categoria", "")
        context["busca"] = self.request.GET.get("q", "")
        return context


def produto_detalhe(request, slug):
    produto = get_object_or_404(Produto, slug=slug, disponivel=True)
    produtos_relacionados = Produto.objects.filter(
        categoria=produto.categoria, disponivel=True
    ).exclude(id=produto.id)[:4]

    context = {"produto": produto, "produtos_relacionados": produtos_relacionados}
    return render(request, "loja/produto_detalhe.html", context)


# Views de administração (página secreta)
def admin_login(request):
    if request.method == "POST":
        senha = request.POST.get("senha")
        if senha == "admin123":  # Senha simples para a dona da loja
            request.session["admin_logado"] = True
            return redirect("loja:admin_dashboard")
        else:
            messages.error(request, "Senha incorreta!")

    return render(request, "loja/admin_login.html")


def admin_dashboard(request):
    if not request.session.get("admin_logado"):
        return redirect("loja:admin_login")

    produtos = Produto.objects.all().order_by("-criado_em")
    categorias = Categoria.objects.all()

    context = {
        "produtos": produtos,
        "categorias": categorias,
        "total_produtos": produtos.count(),
        "produtos_disponiveis": produtos.filter(disponivel=True).count(),
    }
    return render(request, "loja/admin_dashboard.html", context)


def admin_produto_form(request, produto_id=None):
    if not request.session.get("admin_logado"):
        return redirect("loja:admin_login")

    produto = None
    if produto_id:
        produto = get_object_or_404(Produto, id=produto_id)

    if request.method == "POST":
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        formset = ProdutoImagemFormSet(
            request.POST,
            request.FILES,
            queryset=produto.imagens.all() if produto else ProdutoImagem.objects.none(),
        )

        if form.is_valid() and formset.is_valid():
            produto_salvo = form.save()

            # Salvar imagens
            for form_imagem in formset:
                if form_imagem.cleaned_data and not form_imagem.cleaned_data.get(
                    "DELETE", False
                ):
                    if form_imagem.cleaned_data.get("imagem"):
                        imagem = form_imagem.save(commit=False)
                        imagem.produto = produto_salvo
                        imagem.save()

            # Deletar imagens marcadas para exclusão
            for form_imagem in formset.deleted_forms:
                if form_imagem.instance.pk:
                    form_imagem.instance.delete()

            messages.success(request, "Produto salvo com sucesso!")
            return redirect("loja:admin_dashboard")
    else:
        form = ProdutoForm(instance=produto)
        formset = ProdutoImagemFormSet(
            queryset=produto.imagens.all() if produto else ProdutoImagem.objects.none()
        )

    context = {
        "form": form,
        "formset": formset,
        "produto": produto,
    }
    return render(request, "loja/admin_produto_form.html", context)


def admin_produto_delete(request, produto_id):
    if not request.session.get("admin_logado"):
        return redirect("loja:admin_login")

    produto = get_object_or_404(Produto, id=produto_id)
    produto.delete()
    messages.success(request, "Produto excluído com sucesso!")
    return redirect("loja:admin_dashboard")


def admin_categoria_form(request):
    if not request.session.get("admin_logado"):
        return redirect("loja:admin_login")

    if request.method == "POST":
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoria criada com sucesso!")
            return redirect("loja:admin_dashboard")
    else:
        form = CategoriaForm()

    context = {"form": form}
    return render(request, "loja/admin_categoria_form.html", context)
