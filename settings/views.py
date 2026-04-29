from django.shortcuts import render
from .models import Settings
# Create your views here.

# Criando view da home
def home (request):
    
    return render (request, 'home.html')