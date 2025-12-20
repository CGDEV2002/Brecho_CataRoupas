from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Produto, Categoria
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ProdutoSerializer, ProdutoListSerializer, CategoriaSerializer


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


# API Views
class CategoriaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para Categorias
    - GET /api/categorias/ - Lista todas as categorias
    - GET /api/categorias/{id}/ - Detalhe de uma categoria
    """

    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    lookup_field = "slug"


class ProdutoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Produtos
    - GET /api/produtos/ - Lista produtos (público)
    - POST /api/produtos/ - Criar produto (apenas admin)
    - GET /api/produtos/{id}/ - Detalhe do produto (público)
    - PUT /api/produtos/{id}/ - Atualizar produto (apenas admin)
    - DELETE /api/produtos/{id}/ - Deletar produto (apenas admin)
    """

    queryset = Produto.objects.filter(disponivel=True).select_related("categoria")
    serializer_class = ProdutoSerializer
    lookup_field = "slug"

    # Configuração de filtros
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["categoria", "tamanho", "condicao"]
    search_fields = ["nome", "descricao"]
    ordering_fields = ["preco"]
    ordering = ["nome"]

    def get_serializer_class(self):
        """Usar serializer simplificado para listagem"""
        if self.action == "list":
            return ProdutoListSerializer
        return ProdutoSerializer

    @action(detail=False, methods=["get"])
    def por_categoria(self, request):
        """Endpoint customizado: /api/produtos/por_categoria/"""
        categorias = Categoria.objects.all()
        resultado = {}
        for categoria in categorias:
            produtos = self.queryset.filter(categoria=categoria)[:4]
            resultado[categoria.nome] = ProdutoListSerializer(produtos, many=True).data
        return Response(resultado)

    @action(detail=False, methods=["get"])
    def destaques(self, request):
        """Endpoint customizado: /api/produtos/destaques/"""
        produtos = self.queryset.order_by("?")[:6]  # 6 produtos aleatórios
        serializer = ProdutoListSerializer(produtos, many=True)
        return Response(serializer.data)
