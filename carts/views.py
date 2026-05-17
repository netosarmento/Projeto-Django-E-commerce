from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from products.models import Products  # Importa do seu app products
from .models import Cart, CartItem

# Create your views here.

def get_or_create_cart(request):
    
    if request.user.is_authenticated:
        # Usuário logado: busca ou cria carrinho vinculado ao user
        cart, created = Cart.objects.get_or_create(user=request.user)
        return cart
    else:
        # Usuário anônimo: usa session_key
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
        return cart


def cart_detail(request):
    
    cart = get_or_create_cart(request)
    
    context = {
        'cart': cart,
        'cart_items': cart.items.all(),
        'total_price': cart.get_total_price(),
        'total_items': cart.get_total_items(),
    }
    
    return render(request, 'carts/cart_detail.html', context)


@require_POST
def add_to_cart(request, product_id):
    
    product = get_object_or_404(Products, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    
    cart = get_or_create_cart(request)
    
    # Verifica se o produto já está no carrinho
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    
    if not created:
        # Se já existe, aumenta a quantidade
        cart_item.quantity += quantity
        cart_item.save()
        message = f'Quantidade de {product.name} atualizada no carrinho!'
    else:
        message = f'{product.name} adicionado ao carrinho!'
    
    messages.success(request, message)
    
    # Verifica se é requisição AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': message,
            'cart_total_items': cart.get_total_items(),
            'cart_total_price': float(cart.get_total_price()),
        })
    
    return redirect('carts:cart_detail')


@require_POST
def update_cart_item(request, item_id):
   
    cart_item = get_object_or_404(CartItem, id=item_id)
    
    # Verifica se o carrinho pertence ao usuário/sessão atual
    current_cart = get_or_create_cart(request)
    if cart_item.cart != current_cart:
        messages.error(request, 'Item não encontrado no seu carrinho!')
        return redirect('carts:cart_detail')
    
    quantity = int(request.POST.get('quantity', 0))
    
    if quantity <= 0:
        cart_item.delete()
        message = f'{cart_item.product.name} removido do carrinho!'
    else:
        cart_item.quantity = quantity
        cart_item.save()
        message = f'Quantidade de {cart_item.product.name} atualizada!'
    
    messages.success(request, message)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': message,
            'item_total': float(cart_item.get_total_price()),
            'cart_total': float(current_cart.get_total_price()),
            'cart_total_items': current_cart.get_total_items(),
        })
    
    return redirect('carts:cart_detail')


@require_POST
def remove_from_cart(request, item_id):
   
    cart_item = get_object_or_404(CartItem, id=item_id)
    product_name = cart_item.product.name
    
    current_cart = get_or_create_cart(request)
    
    if cart_item.cart == current_cart:
        cart_item.delete()
        messages.success(request, f'{product_name} removido do carrinho!')
    else:
        messages.error(request, 'Item não encontrado no seu carrinho!')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f'{product_name} removido do carrinho!',
            'cart_total': float(current_cart.get_total_price()),
            'cart_total_items': current_cart.get_total_items(),
        })
    
    return redirect('carts:cart_detail')


def clear_cart(request):
   
    cart = get_or_create_cart(request)
    cart.clear_cart()
    messages.success(request, 'Carrinho limpo com sucesso!')
    
    return redirect('carts:cart_detail')


@login_required
def merge_cart_after_login(request):
    
    if request.user.is_authenticated and request.session.session_key:
        session_key = request.session.session_key
        session_cart = Cart.objects.filter(session_key=session_key).first()
        user_cart, created = Cart.objects.get_or_create(user=request.user)
        
        if session_cart:
            # Mescla os itens do carrinho da sessão com o do usuário
            for session_item in session_cart.items.all():
                user_item, created = CartItem.objects.get_or_create(
                    cart=user_cart,
                    product=session_item.product,
                    defaults={'quantity': session_item.quantity}
                )
                if not created:
                    user_item.quantity += session_item.quantity
                    user_item.save()
            
            # Remove o carrinho da sessão
            session_cart.delete()
            messages.success(request, 'Seu carrinho anterior foi mantido!')
    
    return redirect('carts:cart_detail')