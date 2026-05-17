from django.shortcuts import render
from settings.models import Settings, Banner, Propaganda, Carrossel
from products.models import Products, ProductImage, ProductReview, Category

def home(request):
    categorias = Category.objects.filter(products__isnull=False).distinct()
    
    categorias_com_produtos = []
    for categoria in categorias:
        produtos = Products.objects.filter(category=categoria)[:5]  # 5 produtos por categoria
        if produtos.exists():
            categorias_com_produtos.append({
                'categoria': categoria,
                'produtos': produtos
            })
    
    context = {
        'mysettings': Settings.objects.first(),
        'banners': Banner.objects.filter(is_active=True)[:5],
        'propagandas': Propaganda.objects.filter(is_active=True)[:3],
        'carrossel_itens': Carrossel.objects.filter(is_active=True),
        'categorias_com_produtos': categorias_com_produtos,  # ← ADICIONE ESTA LINHA
    }
    return render(request, 'home.html', context)

def contact (request):
    
    return render(request, 'contato.html')

# Desenvolvimento 

# @norte_dev
# Developed by: Tech Norte Soluções
# Instagram: norte_dev
# MEI instagram: @tech.nortesolucoes