from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    image = models.ImageField(upload_to='categories/')

    def __str__(self):
        return self.name

class Products(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    unit = models.IntegerField(default=1)  
    slug = models.SlugField()  
    image = models.ImageField(upload_to='products/')
    
    category = models.ForeignKey(
        'Category', 
        related_name='categorys', 
        on_delete=models.CASCADE
    )
    created_at = models.DateField(default=timezone.now)

    def __str__(self):
        return self.name
    

class ProductReview(models.Model):
    author = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE, verbose_name='autor')
    product = models.ForeignKey(Products, related_name='reviews', on_delete=models.CASCADE)  
    rate = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Avaliação de 1 a 5 estrelas"
    )
    feedback = models.TextField(max_length=2000, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']  

    def __str__(self):
        return f"Review {self.rate}/5 for {self.product.name} by {self.author.username}"  