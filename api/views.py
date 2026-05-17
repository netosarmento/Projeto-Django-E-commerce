from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q, Count, Avg
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta

from .serializers import *
from products.models import Category, Products, ProductReview
from orders.models import Order, OrderItem
from carts.models import Cart, CartItem
from django.contrib.auth.models import User

# Import settings models (ajuste o nome do seu app)
from settings.models import Settings, Banner, Propaganda, Carrossel  # Ajuste!

# ============ CONFIGURAÇÕES E HOME ============

class SettingsAPIView(APIView):
    """Retorna configurações do site"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        settings = Settings.objects.first()
        if not settings:
            return Response({'error': 'Configurações não encontradas'}, status=404)
        serializer = SettingsSerializer(settings)
        return Response(serializer.data)

class HomeAPIView(APIView):
    """Retorna todos os dados da página inicial"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        settings = Settings.objects.first()
        banners = Banner.objects.filter(is_active=True)
        carrossel = Carrossel.objects.filter(is_active=True)
        propagandas = Propaganda.objects.filter(is_active=True)
        
        # Produtos em destaque (últimos 8)
        featured_products = Products.objects.all().order_by('-created_at')[:8]
        
        # Produtos novos (últimos 7 dias)
        last_week = timezone.now() - timedelta(days=7)
        new_products = Products.objects.filter(created_at__gte=last_week)[:4]
        
        # Categorias com contagem
        categories = Category.objects.annotate(product_count=Count('products')).filter(product_count__gt=0)
        
        # Estatísticas
        total_products = Products.objects.count()
        total_users = User.objects.count()
        
        data = {
            'settings': settings,
            'banners': banners,
            'carrossel': carrossel,
            'propagandas': propagandas,
            'featured_products': featured_products,
            'new_products': new_products,
            'categories': categories,
            'total_products': total_products,
            'total_users': total_users,
        }
        
        serializer = HomeSerializer(data)
        return Response(serializer.data)

# ============ PRODUTOS ============

class ProductListAPIView(APIView):
    """Lista produtos com filtros"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        products = Products.objects.all()
        
        # Filtros
        category_id = request.GET.get('category')
        if category_id:
            products = products.filter(category_id=category_id)
        
        search = request.GET.get('search')
        if search:
            products = products.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )
        
        min_price = request.GET.get('min_price')
        if min_price:
            products = products.filter(price__gte=min_price)
        
        max_price = request.GET.get('max_price')
        if max_price:
            products = products.filter(price__lte=max_price)
        
        # Ordenação
        ordering = request.GET.get('ordering', '-created_at')
        allowed = ['name', '-name', 'price', '-price', 'created_at', '-created_at']
        if ordering in allowed:
            products = products.order_by(ordering)
        
        # Paginação
        limit = int(request.GET.get('limit', 20))
        products = products[:limit]
        
        serializer = ProductListSerializer(products, many=True)
        return Response({
            'count': products.count(),
            'results': serializer.data
        })

class ProductDetailAPIView(RetrieveAPIView):
    """Detalhes de um produto"""
    permission_classes = [AllowAny]
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'

class ProductReviewsAPIView(APIView):
    """CRUD de avaliações"""
    
    def get(self, request, slug):
        product = get_object_or_404(Products, slug=slug)
        reviews = product.reviews.all()[:10]
        serializer = ProductReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    
    def post(self, request, slug):
        if not request.user.is_authenticated:
            return Response({'error': 'Faça login para avaliar'}, status=401)
        
        product = get_object_or_404(Products, slug=slug)
        
        if ProductReview.objects.filter(author=request.user, product=product).exists():
            return Response({'error': 'Você já avaliou este produto'}, status=400)
        
        serializer = ProductReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, product=product)
            return Response(serializer.data, status=201)
        
        return Response(serializer.errors, status=400)

class CategoriesAPIView(ListAPIView):
    """Lista categorias"""
    permission_classes = [AllowAny]
    queryset = Category.objects.annotate(product_count=Count('products')).filter(product_count__gt=0)
    serializer_class = CategorySerializer

class SearchAPIView(APIView):
    """Busca avançada"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        query = request.GET.get('q', '').strip()
        
        if not query or len(query) < 2:
            return Response({'results': [], 'message': 'Digite pelo menos 2 caracteres'})
        
        products = Products.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )[:20]
        
        serializer = ProductListSerializer(products, many=True)
        return Response({
            'query': query,
            'count': products.count(),
            'results': serializer.data
        })

# ============ CARRINHO ============

class CartAPIView(APIView):
    """Gerenciar carrinho"""
    permission_classes = [IsAuthenticated]
    
    def get_cart(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        return cart
    
    def get(self, request):
        cart = self.get_cart(request)
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    
    def post(self, request):
        """Adicionar produto ao carrinho"""
        cart = self.get_cart(request)
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        
        product = get_object_or_404(Products, id=product_id)
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=201)
    
    def put(self, request, item_id):
        """Atualizar quantidade de um item"""
        cart = self.get_cart(request)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        
        quantity = request.data.get('quantity')
        if quantity:
            cart_item.quantity = int(quantity)
            cart_item.save()
        
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    
    def delete(self, request, item_id):
        """Remover item do carrinho"""
        cart = self.get_cart(request)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        cart_item.delete()
        
        serializer = CartSerializer(cart)
        return Response(serializer.data)

class CartClearAPIView(APIView):
    """Limpar todo o carrinho"""
    permission_classes = [IsAuthenticated]
    
    def delete(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart.clear_cart()
        return Response({'message': 'Carrinho limpo com sucesso'})

# ============ PEDIDOS ============

class OrderListAPIView(APIView):
    """Listar pedidos do usuário"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

class OrderDetailAPIView(APIView):
    """Detalhes de um pedido"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

class CreateOrderAPIView(APIView):
    """Criar pedido a partir do carrinho"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        cart = Cart.objects.filter(user=request.user).first()
        
        if not cart or not cart.items.exists():
            return Response({'error': 'Carrinho vazio'}, status=400)
        
        serializer = CreateOrderSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        
        # Calcular valores
        subtotal = cart.get_total_price()
        shipping_cost = 10.00  # Valor fixo ou calculado
        discount = 0
        total_amount = subtotal + shipping_cost - discount
        
        # Criar pedido
        order = Order.objects.create(
            user=request.user,
            subtotal=subtotal,
            shipping_cost=shipping_cost,
            discount=discount,
            total_amount=total_amount,
            **serializer.validated_data
        )
        
        # Criar itens do pedido
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
        
        # Limpar carrinho
        cart.clear_cart()
        
        order_serializer = OrderSerializer(order)
        return Response(order_serializer.data, status=201)

# ============ USUÁRIOS ============

class UserProfileAPIView(APIView):
    """Perfil do usuário autenticado"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        profile, created = Profile.objects.get_or_create(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
    
    def put(self, request):
        profile = request.user.profile
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

# Desenvolvimento 

# @norte_dev

# Developed by: Tech Norte Soluções
# Instagram: norte_dev
# MEI instagram: @tech.nortesolucoes