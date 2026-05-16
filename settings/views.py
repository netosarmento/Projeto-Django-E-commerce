from django.shortcuts import render
from settings.models import Settings, Banner, Propaganda

def home(request):
    context = {
        'mysettings': Settings.objects.first(),
        'banners': Banner.objects.filter(is_active=True)[:5],  # Pega até 5 banners ativos
        'propagandas': Propaganda.objects.filter(is_active=True)[:3],  # Pega até 3 propagandas
    }
    return render(request, 'home.html', context)  # ou o nome do seu template

def contact (request):
    
    return render(request, 'contato.html')

# Desenvolvimento 

# @norte_dev