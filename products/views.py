from django.shortcuts import render, get_object_or_404, redirect
from .models import ProductReview, Products, Category, ProductImage
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg
from django.db.models import Q
# Create your views here.

def category_products_view(request):
    
    # Pega 3 categorias que tenham pelo menos 1 produto
    categorias = Category.objects.filter(products__isnull=False).distinct()[:3]
    
    produtos_por_categoria = {}
    
    for categoria in categorias:
        
        produtos = Products.objects.filter(category=categoria).prefetch_related('images', 'reviews')[:3]
        
        produtos_com_info = []
        for produto in produtos:
            media_avaliacoes = produto.reviews.aggregate(Avg('rate'))['rate__avg']
            produtos_com_info.append({
                'produto': produto,
                'media_avaliacoes': media_avaliacoes if media_avaliacoes else 0,
                'total_avaliacoes': produto.reviews.count(),
                'imagens_extras': produto.images.all()[:1]  
            })
        
        produtos_por_categoria[categoria] = produtos_com_info
    
    context = {
        'produtos_por_categoria': produtos_por_categoria,
    }
    
    return render(request, 'category_products.html', context)

# Review dos usuários 
def products_view(request, slug):
    product = get_object_or_404(Products, slug=slug)
    product_category = Products.objects.filter(category=product.category).exclude(slug=product.slug)[:4]
    reviews = ProductReview.objects.filter(product=product)
    imagens_extras = product.images.all()
    
    context = {
        'product': product,
        'product_category': product_category,
        'reviews': reviews,
        'imagens_extras': imagens_extras,
    }
    
    return render(request, 'product_detail.html', context)


@login_required
def add_review(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    
    if request.method == 'POST':
        rate = request.POST.get('rate')
        feedback = request.POST.get('feedback')
        
        existing_review = ProductReview.objects.filter(author=request.user, product=product).first()
        
        if existing_review:
            messages.warning(request, 'Você já avaliou este produto!')
        else:
            ProductReview.objects.create(
                author=request.user,
                product=product,
                rate=rate,
                feedback=feedback
            )
            messages.success(request, 'Avaliação enviada com sucesso!')
    
    return redirect('products:products_view', slug=product.slug)

def product_list(request):
    # Pega parâmetro de busca
    query = request.GET.get('q', '')
    
    # Base da query
    products_query = Products.objects.all()
    
    # Aplica filtro de busca se existir
    if query and len(query) >= 2:
        products_query = products_query.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )
    
    # Busca categorias com produtos (filtradas ou não)
    if query:
        # Se está buscando, mostra produtos encontrados agrupados
        categorias = Category.objects.filter(products__in=products_query).distinct()
    else:
        categorias = Category.objects.filter(products__isnull=False).distinct()
    
    categorias_com_produtos = []
    for categoria in categorias:
        produtos = products_query.filter(category=categoria)[:5]
        if produtos.exists():
            categorias_com_produtos.append({
                'categoria': categoria,
                'produtos': produtos
            })
    
    context = {
        'categorias_com_produtos': categorias_com_produtos,
        'query': query,
        'has_query': bool(query),
        'total_results': products_query.count() if query else None,
    }
    return render(request, 'product_list.html', context)

def search_products(request):
    """View para busca de produtos (recarrega página)"""
    query = request.GET.get('q', '').strip()
    products = []
    
    if query:
        if len(query) >= 2:
            products = Products.objects.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(category__name__icontains=query)
            ).prefetch_related('images', 'reviews')
            
            # Adiciona média de avaliações para cada produto
            for product in products:
                product.avg_rating = product.reviews.aggregate(Avg('rate'))['rate__avg'] or 0
                product.reviews_count = product.reviews.count()
    
    context = {
        'query': query,
        'products': products,
        'total_results': products.count() if query else 0,
        'has_results': len(products) > 0 if query else False,
    }
    
    return render(request, 'search_results.html', context)

# Desenvolvimento 

# @norte_dev
# Developed by: Tech Norte Soluções
# Instagram: norte_dev
# MEI instagram: @tech.nortesolucoes
