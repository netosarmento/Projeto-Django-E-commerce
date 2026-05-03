from django.urls import path
from . import views

app_name = 'carts'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('adicionar/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('atualizar/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('remover/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('limpar/', views.clear_cart, name='clear_cart'),
    path('mesclar/', views.merge_cart_after_login, name='merge_cart'),
]