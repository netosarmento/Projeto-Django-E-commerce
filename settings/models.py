from django.db import models
from django.utils import timezone
# Create your models here.

# Criando váriaveis 
class Settings (models.Model):

    site_name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to="settings/")
    phone = models.CharField(max_length=11)
    email = models.EmailField(max_length=200)
    description = models.TextField(max_length=300)
    fb_link = models.URLField(max_length=200)
    inst_link = models.URLField(max_length=200)
    address = models.CharField(max_length=200,default="Belém, Pará")

    def __str__(self): 
        return self.site_name