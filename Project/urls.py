"""
URL configuration for Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from settings.views import home, contact

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', home , name='home'),
    path('', contact , name='contatos'),
    path('contas/', include(('users.urls', 'users'), namespace='users')),
    path('pedidos/', include(('orders.urls', 'orders'), namespace='orders')),
    path('', include(('settings.urls', 'settings'), namespace='home')),
    path('produtos/', include(('products.urls', 'products'), namespace='products')),
    path('carrinho/', include(('carts.urls', 'carts'), namespace='carts')),
]


# Configuração para arquivos estáticos e mídia (modo DEV)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Desenvolvimento 

# @norte_dev

# Developed by: Tech Norte Soluções
# Instagram: norte_dev
# MEI instagram: @tech.nortesolucoes