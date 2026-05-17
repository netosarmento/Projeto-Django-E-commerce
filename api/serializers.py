from rest_framework import serializers
from django.contrib.auth.models import User
from django.db.models import Avg, Count

# Import dos models
from products.models import Category, Products, ProductImage, ProductReview
from orders.models import Order, OrderItem
from carts.models import Cart, CartItem
from users.models import Profile

# Import dos models de configuração (ajuste o nome do seu app)
from settings.models import Settings, Banner, Propaganda, Carrossel  # Ajuste o app!

# ============ USERS ============
class UserSerializer(serializers.ModelSerializer):
    """Serializa usuário básico"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']

class ProfileSerializer(serializers.ModelSerializer):
    """Serializa perfil do usuário"""
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = Profile
        fields = ['id', 'username', 'email', 'image']

# ============ SETTINGS ============
class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = ['site_name', 'logo', 'phone', 'email', 'description', 
                 'fb_link', 'inst_link', 'address']

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id', 'title', 'image', 'link', 'order', 'is_active']

class PropagandaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Propaganda
        fields = ['id', 'title', 'image', 'link', 'order', 'is_active']

class CarrosselSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrossel
        fields = ['id', 'title', 'image', 'link', 'order', 'is_active']

# ============ PRODUTOS ============
class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'image', 'product_count']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text']

class ProductReviewSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    
    class Meta:
        model = ProductReview
        fields = ['id', 'author_name', 'rate', 'feedback', 'created_at']
        read_only_fields = ['author', 'created_at']

class ProductSerializer(serializers.ModelSerializer):
    """Serializer completo do produto"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_id = serializers.IntegerField(source='category.id', read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()
    reviews = ProductReviewSerializer(many=True, read_only=True)
    
    class Meta:
        model = Products
        fields = [
            'id', 'name', 'description', 'unit', 'price', 'slug', 
            'image', 'category', 'category_name', 'category_id',
            'created_at', 'images', 'average_rating', 'reviews_count', 'reviews'
        ]
    
    def get_average_rating(self, obj):
        result = obj.reviews.aggregate(avg=Avg('rate'))
        return round(result['avg'], 1) if result['avg'] else 0
    
    def get_reviews_count(self, obj):
        return obj.reviews.count()

class ProductListSerializer(serializers.ModelSerializer):
    """Versão leve para listagens (mais rápido)"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    average_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Products
        fields = ['id', 'name', 'price', 'slug', 'image', 'category_name', 'average_rating']
    
    def get_average_rating(self, obj):
        result = obj.reviews.aggregate(avg=Avg('rate'))
        return round(result['avg'], 1) if result['avg'] else 0

# ============ CARRINHO ============
class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', read_only=True, max_digits=10, decimal_places=2)
    product_image = serializers.ImageField(source='product.image', read_only=True)
    product_slug = serializers.CharField(source='product.slug', read_only=True)
    subtotal = serializers.SerializerMethodField()
    
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_name', 'product_price', 
                 'product_image', 'product_slug', 'quantity', 'subtotal']
    
    def get_subtotal(self, obj):
        return obj.get_total_price()

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.DecimalField(source='get_total_price', read_only=True, max_digits=10, decimal_places=2)
    total_items = serializers.IntegerField(source='get_total_items', read_only=True)
    
    class Meta:
        model = Cart
        fields = ['id', 'items', 'total', 'total_items', 'created_at', 'updated_at']

class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1, default=1)

class UpdateCartItemSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)

# ============ PEDIDOS ============
class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_image = serializers.ImageField(source='product.image', read_only=True)
    product_slug = serializers.CharField(source='product.slug', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'product_image', 
                 'product_slug', 'quantity', 'price', 'get_total']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'user', 'user_name', 'created_at', 'updated_at', 
            'status', 'status_display', 'subtotal', 'shipping_cost',
            'discount', 'total_amount', 'shipping_address', 'shipping_city',
            'shipping_state', 'shipping_zip_code', 'shipping_phone',
            'payment_method', 'notes', 'items'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at', 'subtotal', 'total_amount']

class CreateOrderSerializer(serializers.Serializer):
    shipping_address = serializers.CharField(max_length=500)
    shipping_city = serializers.CharField(max_length=100)
    shipping_state = serializers.CharField(max_length=50)
    shipping_zip_code = serializers.CharField(max_length=20)
    shipping_phone = serializers.CharField(max_length=20)
    payment_method = serializers.CharField(max_length=50, required=False, allow_blank=True)
    notes = serializers.CharField(required=False, allow_blank=True)

# ============ HOME (PÁGINA INICIAL) ============
class HomeSerializer(serializers.Serializer):
    settings = SettingsSerializer()
    banners = BannerSerializer(many=True)
    carrossel = CarrosselSerializer(many=True)
    propagandas = PropagandaSerializer(many=True)
    featured_products = ProductListSerializer(many=True)
    new_products = ProductListSerializer(many=True)
    categories = CategorySerializer(many=True)
    total_products = serializers.IntegerField()
    total_users = serializers.IntegerField()
    
    
# Desenvolvimento 

# @norte_dev

# Developed by: Tech Norte Soluções
# Instagram: norte_dev
# MEI instagram: @tech.nortesolucoes