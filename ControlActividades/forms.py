from django.forms import ModelForm,widgets, Textarea
from django import forms
from ControlActividades.models import *

class ProyectosForm(forms.ModelForm):
	class Meta:
		model = Proyectos
		fields = ('Proyecto', 'Usuario', 'Estatus')
		widgets = {
		'Proyecto': widgets.TextInput(attrs={"autofocus":True,"placeholder" : 'Proyecto', "maxlength" : '40' ,'title':'proyecto','required':True}),
		'Usuario': widgets.Select(attrs={"placeholder" : 'Selecione','title':'Usuario','required':True}),
		'Estatus': widgets.HiddenInput(attrs={'required':True,'disabled':True}),
		}

class ActividadForm(forms.ModelForm):
	class Meta:
		model = Actividad
		fields = ('Actividad','Desde', 'Hasta', 'Estatus','Proyecto','Usuario','FechaSolicitud','Solicitud','Observaciones')
		widgets = {
		'Actividad': widgets.TextInput(attrs={"autofocus":True,"placeholder" : 'Actividad', "maxlength" : '40' ,'title':'Actividad','required':True}),
		'Desde': widgets.TextInput(attrs={"placeholder" : 'Fecha Inicial','title':'Desde','required':True}),
		'Hasta': widgets.TextInput(attrs={"placeholder" : 'Fecha Terminal','title':'Hasta','required':True}),
		'Estatus': widgets.HiddenInput(attrs={'required':True,'disabled':True}),
		'Proyecto': widgets.HiddenInput(attrs={'required':True,'disabled':True}),
		'Usuario': widgets.Select(attrs={"placeholder" : 'Selecione Usuario','title':'Usuario','required':True}),
		'FechaSolicitud': widgets.TextInput(attrs={"placeholder" : 'Fecha de solicitud','title':'Fecha de Solicitud','required':True}),
		'Solicitud': widgets.TextInput(attrs={"placeholder" : 'Solicitante','title':'Solicitante','required':True}),
		}
		
class AvancesForm(forms.ModelForm):
	class Meta:
		model = Avances
		fields = ('Avance','Points','Actividad','Estatus')
		widgets = {
		'Avance': widgets.Textarea(attrs={"autofocus":True,"placeholder" : 'Avance', "maxlength" : '500' ,'title':'Avance','required':True}),
		'Points': widgets.TextInput(attrs={"placeholder" : 'puntuacion','title':'Puntos','required':True}),
		'Actividad':  widgets.HiddenInput(attrs={'required':True,'disabled':True}),
		'Estatus': widgets.HiddenInput(attrs={'required':True,'disabled':True}),
		}

class CancelacionForm(forms.ModelForm):
	class Meta:
		model = Cancelacion
		fields = ('motivo','Observacion','Estatus','Usuario','actividad')
		widgets = {
		'motivo': widgets.TextInput(attrs={"autofocus":True,"placeholder" : 'Motivo', "maxlength" : '100' ,'title':'motivo','required':True}),
		'Observacion': Textarea(attrs={"placeholder" : 'Por que?','cols': 150,'required':True, 'rows': 10}),
		'Usuario': widgets.HiddenInput(attrs={'title':'Usuario','required':True,'disabled':True}),
		'actividad': widgets.HiddenInput(attrs={'title':'Actividad','required':True,'disabled':True}),
		'Estatus': widgets.HiddenInput(attrs={'required':True,'disabled':True}),
		}
		
class NotificacionesForm(forms.ModelForm):
	class Meta:
		model = Notificaciones
		fields = ('Descripcion','Tipo','Usuario','Envio','Estatus')
		widgets = {
		'Descripcion': Textarea(attrs={"placeholder" : 'Por que?','style':'width:100%;','required':True}),
		'Tipo': widgets.HiddenInput(attrs={"placeholder" : 'Tipo','required':True,}),
		'Usuario': widgets.HiddenInput(attrs={'title':'Usuario','required':True,'disabled':True}),
		'Envio': widgets.HiddenInput(attrs={'title':'Actividad','required':True,'disabled':True}),
		'Estatus': widgets.HiddenInput(attrs={'required':True,'disabled':True}),
		}
