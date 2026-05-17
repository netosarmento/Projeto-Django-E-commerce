from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class Cart(models.Model):

    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='cart',
        null=True, 
        blank=True
    )
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        if self.user:
            return f"Carrinho de {self.user.username}"
        return f"Carrinho da sessão: {self.session_key}"
    
    def get_total_price(self):
        
        total = sum(item.get_total_price() for item in self.items.all())
        return total
    
    def get_total_items(self):
        
        return sum(item.quantity for item in self.items.all())
    
    def clear_cart(self):
        
        self.items.all().delete()


class CartItem(models.Model):
    
    cart = models.ForeignKey(
        Cart, 
        on_delete=models.CASCADE, 
        related_name='items'
    )
    product = models.ForeignKey(
        'products.Products', 
        on_delete=models.CASCADE,
        related_name='cart_items'
    )
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-added_at']
        unique_together = ['cart', 'product']  
    
    def __str__(self):
        return f"{self.quantity}x {self.product.name} no carrinho {self.cart.id}"
    
    def get_total_price(self):
        price = getattr(self.product, 'price', self.product.unit)
        return self.quantity * price
    
    def increase_quantity(self, amount=1):
        
        self.quantity += amount
        self.save()
    
    def decrease_quantity(self, amount=1):
        
        if self.quantity > amount:
            self.quantity -= amount
            self.save()
        else:
            self.delete()  