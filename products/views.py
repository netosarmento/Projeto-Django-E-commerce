from django.shortcuts import render, get_object_or_404, redirect
from .models import ProductReview, Products, Category, ProductImage
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg

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

# Criar a lista de products da Home
def product_list(request):
    # Busca todas as categorias que têm produtos ativos
    categorias = Category.objects.filter(products__isnull=False).distinct()
    
    # Para cada categoria, pega os produtos
    categorias_com_produtos = []
    for categoria in categorias:
        produtos = Products.objects.filter(category=categoria)[:5]  # Limita a 5 por linha
        if produtos.exists():
            categorias_com_produtos.append({
                'categoria': categoria,
                'produtos': produtos
            })
    
    context = {
        'categorias_com_produtos': categorias_com_produtos,
    }
    return render(request, 'products/product_list.html', context)