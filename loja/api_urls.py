from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Criar router para URLs automáticas
router = DefaultRouter()
router.register(r"produtos", views.ProdutoViewSet)
router.register(r"categorias", views.CategoriaViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
