from django.db import models
from django.utils import timezone

# Create your models here
# Criando todas as personalizações

class Settings(models.Model):
    site_name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to="settings/")
    phone = models.CharField(max_length=11)
    email = models.EmailField(max_length=200)
    description = models.TextField(max_length=300)
    fb_link = models.URLField(max_length=200)
    inst_link = models.URLField(max_length=200)
    address = models.CharField(max_length=200, default="Belém, Pará")

    def __str__(self): 
        return self.site_name


# BANNER PRINCIPAL
class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name="Título do Banner")
    image = models.ImageField(upload_to="banners/", verbose_name="Imagem do Banner")
    link = models.URLField(blank=True, null=True, verbose_name="Link do Banner")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    order = models.IntegerField(default=0, verbose_name="Ordem")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Banner"
        verbose_name_plural = "Banners"


# Model Propaganda
class Propaganda(models.Model):
    title = models.CharField(max_length=100, verbose_name="Título")
    image = models.ImageField(upload_to="propagandas/", verbose_name="Imagem")
    link = models.URLField(blank=True, null=True, verbose_name="Link")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    order = models.IntegerField(default=0, verbose_name="Ordem (1, 2, 3)")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']
        verbose_name = "Propaganda"
        verbose_name_plural = "Propagandas"
        
# Carrosel Home        
class Carrossel(models.Model):
    title = models.CharField(max_length=100, verbose_name="Título da Imagem")
    image = models.ImageField(upload_to="carrossel/", verbose_name="Imagem do Carrossel")
    link = models.URLField(blank=True, null=True, verbose_name="Link (opcional)")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    order = models.IntegerField(default=0, verbose_name="Ordem (1, 2, 3...)")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = "Carrossel"
        verbose_name_plural = "Carrossel"