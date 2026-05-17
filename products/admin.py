from django.contrib import admin
from .models import ProductReview, Products, Category
# Register your models here.


admin.site.register(ProductReview)
admin.site.register(Products)
admin.site.register(Category)