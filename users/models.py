from django.db import models
from django.contrib.auth.models import User
from PIL import Image, ExifTags
import os 

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    def __str__(self):
        return f'{self.user.username} profile'
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if os.path.basename(self.image.path) == 'default.jpg':
            return 

        if not os.path.exists(self.image.path):
            return 

        # Abre a imagem do perfil (agora sabemos que ela existe e não é a padrão)
        img = Image.open(self.image.path)

        try:
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    exif = img._getexif()
                    if exif is not None:
                        orientation_value = exif.get(orientation)
                        if orientation_value == 3:
                            img = img.rotate(180, expand=True)
                        elif orientation_value == 6:
                            img = img.rotate(270, expand=True)
                        elif orientation_value == 8:
                            img = img.rotate(90, expand=True)
                    break
        except (AttributeError, KeyError, IndexError):
            # Caso a imagem não tenha metadados de orientação, seguimos normalmente
            pass

        # Redimensiona se for maior que 300x300 pixels
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)

        # Salva a imagem processada
        img.save(self.image.path)


# Developed by: Tech Norte Soluções
# Instagram: norte_dev
# MEI instagram: @tech.nortesolucoes