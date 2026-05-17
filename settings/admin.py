from django.contrib import admin
from .models import Settings, Banner, Propaganda, Carrossel

@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'phone', 'email']
    fieldsets = (
        ('Informações Principais', {
            'fields': ('site_name', 'logo', 'description')
        }),
        ('Contato', {
            'fields': ('phone', 'email', 'address')
        }),
        ('Redes Sociais', {
            'fields': ('fb_link', 'inst_link')
        }),
    )


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'order', 'created_at']
    list_editable = ['is_active', 'order']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title']


@admin.register(Propaganda)
class PropagandaAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title']

@admin.register(Carrossel)
class CarrosselAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active', 'created_at']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title']

# Desenvolvimento 

# @norte_dev

# Developed by: Tech Norte Soluções
# Instagram: norte_dev
# MEI instagram: @tech.nortesolucoes
