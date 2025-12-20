from rest_framework import serializers
from .models import Produto, Categoria


class CategoriaSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Categoria"""

    produtos_count = serializers.SerializerMethodField()

    class Meta:
        model = Categoria
        fields = ["id", "nome", "slug", "produtos_count"]

    def get_produtos_count(self, obj):
        return obj.produtos.filter(disponivel=True).count()


class ProdutoSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Produto"""

    categoria_nome = serializers.CharField(source="categoria.nome", read_only=True)

    class Meta:
        model = Produto
        fields = [
            "id",
            "nome",
            "slug",
            "descricao",
            "preco",
            "categoria",
            "categoria_nome",
            "tamanho",
            "condicao",
            "disponivel",
            "imagem",
        ]
        read_only_fields = ["slug"]


class ProdutoListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listagem de produtos"""

    categoria_nome = serializers.CharField(source="categoria.nome", read_only=True)

    class Meta:
        model = Produto
        fields = [
            "id",
            "nome",
            "slug",
            "preco",
            "categoria_nome",
            "tamanho",
            "condicao",
            "imagem",
        ]
