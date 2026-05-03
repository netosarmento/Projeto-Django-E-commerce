from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from carts.models import Cart
from .models import Order, OrderItem

@login_required
def checkout(request):
    cart = get_cart_from_user(request)  
    
    if cart.get_total_items() == 0:
        messages.warning(request, 'Seu carrinho está vazio!')
        return redirect('carts:cart_detail')
    
    if request.method == 'POST':
        with transaction.atomic(): 
            # Cria o pedido
            order = Order.objects.create(
                user=request.user,
                shipping_address=request.POST.get('address'),
                shipping_city=request.POST.get('city'),
                shipping_state=request.POST.get('state'),
                shipping_zip_code=request.POST.get('zip_code'),
                shipping_phone=request.POST.get('phone'),
                payment_method='pending',  # Valor padrão já que não tem pagamento
                subtotal=cart.get_total_price(),
                shipping_cost=9.99,
                total_amount=cart.get_total_price() + 9.99,
                status='pending'  # Status inicial
            )
            
            # Cria os itens do pedido
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )
            
            # Limpa o carrinho
            cart.clear_cart()
            
            messages.success(request, f'Pedido #{order.id} criado com sucesso!')
            return redirect('orders:order_detail', order_id=order.id)
    
    context = {
        'cart': cart,
        'subtotal': cart.get_total_price(),
        'shipping': 9.99,
        'total': cart.get_total_price() + 9.99,
    }
    return render(request, 'orders/checkout.html', context)


@login_required
def order_detail(request, order_id):
    
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
def my_orders(request):
    
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/my_orders.html', {'orders': orders})


def get_cart_from_user(request):
    
    from carts.views import get_or_create_cart
    return get_or_create_cart(request)