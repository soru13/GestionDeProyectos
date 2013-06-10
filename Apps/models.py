from django.db import models
from django.contrib.auth.models import User

class Aplicaciones(models.Model):
    desarrolador = models.ForeignKey(User)
    titulo = models.CharField(max_length=60)
    descripcion = models.TextField()
    App = models.FileField(upload_to='apps')

    