from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Produto, Categoria


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
