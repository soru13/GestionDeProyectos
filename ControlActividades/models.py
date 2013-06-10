# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Proyectos(models.Model):
	Proyecto = models.CharField(max_length=50,unique=True)
	Usuario = models.ForeignKey(User)
	Fecha = models.DateTimeField(auto_now=True)
	Estatus = models.BooleanField(default=True)
	def __unicode__(self):
		return self.Proyecto

class Actividad(models.Model):
	Actividad = models.CharField(max_length=200)
	Fecha = models.DateTimeField(auto_now=True)
	Desde = models.DateField()
	Hasta = models.DateField()
	Proyecto = models.ForeignKey(Proyectos)
	Usuario = models.ForeignKey(User)
	Estatus = models.BooleanField(default=True)
	FechaSolicitud = models.DateField()
	Solicitud = models.CharField(max_length=100)
	Observaciones = models.TextField(max_length=500)
	Proceso = models.BooleanField(default=False)
	Finalizado = models.BooleanField(default=False)
	Cancelado = models.BooleanField(default=False)

	def __unicode__(self):
		return self.Actividad

class Avances(models.Model):
	Avance = models.TextField(max_length=500)
	Fecha = models.DateTimeField(auto_now=True)
	Points = models.IntegerField()
	Actividad = models.ForeignKey(Actividad)
	Estatus = models.BooleanField(default=True)
	def __unicode__(self):
		return self.Avance

class Cancelacion(models.Model):
	motivo = models.CharField(max_length=200)
	Observacion = models.TextField(max_length=500)
	Fecha = models.DateTimeField(auto_now=True)
	Estatus = models.BooleanField(default=True)
	Usuario = models.ForeignKey(User)
	actividad = models.CharField(max_length=200)
	def __unicode__(self):
		return self.motivo

class Notificaciones(models.Model):
	Descripcion = models.CharField(max_length=200)
	Tipo = models.CharField(max_length=200)
	Fecha = models.DateTimeField(auto_now=True)
	Estatus = models.BooleanField(default=False)
	Usuario = models.ForeignKey(User)
	Envio = models.CharField(max_length=100)
	def __unicode__(self):
		return self.Descripcion

