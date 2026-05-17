from django.urls import path
from .views import *

urlpatterns = [
    # Configurações
    path('settings/', SettingsAPIView.as_view(), name='settings'),
    path('home/', HomeAPIView.as_view(), name='home'),
    
    # Produtos
    path('products/', ProductListAPIView.as_view(), name='products'),
    path('products/<slug:slug>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('products/<slug:slug>/reviews/', ProductReviewsAPIView.as_view(), name='product-reviews'),
    path('categories/', CategoriesAPIView.as_view(), name='categories'),
    path('search/', SearchAPIView.as_view(), name='search'),
    
    # Carrinho
    path('cart/', CartAPIView.as_view(), name='cart'),
    path('cart/item/<int:item_id>/', CartAPIView.as_view(), name='cart-item'),
    path('cart/clear/', CartClearAPIView.as_view(), name='cart-clear'),
    
    # Pedidos
    path('orders/', OrderListAPIView.as_view(), name='orders'),
    path('orders/create/', CreateOrderAPIView.as_view(), name='create-order'),
    path('orders/<int:order_id>/', OrderDetailAPIView.as_view(), name='order-detail'),
    
    # Usuários
    path('profile/', UserProfileAPIView.as_view(), name='profile'),
]


# Desenvolvimento 

# @norte_dev

# Developed by: Tech Norte Soluções
# Instagram: norte_dev
# MEI instagram: @tech.nortesolucoes