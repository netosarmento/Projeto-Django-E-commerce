from django.urls import path
from .views import category_products_view, products_view, add_review, product_list


app_name = 'products'

urlpatterns = [
    path('categorias-produtos/', category_products_view, name='category_products'),
    path('produto/<slug:slug>/', products_view, name='products_view'),
    path('adicionar-avaliacao/<int:product_id>/', add_review, name='add_review'),
    path('produtos/', product_list, name='product_list'),
]