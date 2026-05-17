from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Cria automaticamente um perfil (Profile) quando um novo usuário é criado.
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Garante que o perfil (Profile) seja salvo junto com o User.
    Se o perfil não existir (usuários antigos), ele é criado.
    """
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        Profile.objects.create(user=instance)




# Developed by: Tech Norte Soluções
# Instagram: norte_dev
# MEI instagram: @tech.nortesolucoes