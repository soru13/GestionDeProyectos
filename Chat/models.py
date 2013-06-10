from django.db import models
from django.contrib.auth.models import User
from ControlActividades.models import Actividad
from Usuarios.models import Perfil

# Create your models here.
class Mensajeria(models.Model):
	Mensaje = models.TextField(max_length=500)
	Fecha = models.DateTimeField(auto_now=True)
	Estatus = models.BooleanField(default=False)
	Envio = models.ForeignKey(User)
	Actividad = models.ForeignKey(Actividad)
	Recivio = models.CharField(max_length=100)
	avatar=models.ForeignKey(Perfil)
	def __unicode__(self):
		return self.Mensaje

class PeerToPeer(models.Model):
	Mensaje = models.TextField(max_length=500)
	Fecha = models.DateTimeField(auto_now=True)
	Estatus = models.BooleanField(default=False)
	Envio = models.ForeignKey(User)
	Recivio = models.CharField(max_length=100)
	avatar=models.ForeignKey(Perfil)
	def __unicode__(self):
		return self.Mensaje