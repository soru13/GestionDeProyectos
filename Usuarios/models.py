from django.db import models
from django.contrib.auth.models import User


class Perfil(models.Model):
    user = models.OneToOneField(User, unique=True, related_name='perfil')
    avatar = models.ImageField(upload_to='AvatarUser')
    direccion = models.TextField()

    def __unicode__(self):
		return self.direccion
