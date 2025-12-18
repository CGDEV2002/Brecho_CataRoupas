from django.urls import path
from . import views

app_name = "loja"

urlpatterns = [
    path("", views.LojaView.as_view(), name="index"),
    path("produto/<slug:slug>/", views.produto_detalhe, name="produto_detalhe"),
]
