from django.forms import ModelForm,widgets, Textarea
from django import forms
from Chat.models import *

class CorreoForm(forms.ModelForm):
	class Meta:
		model = Mensajeria
		fields = ('Mensaje','Envio','Actividad','Recivio','Estatus','avatar')
		widgets = {
		'Mensaje': widgets.Textarea(attrs={"autofocus":False,"placeholder" : 'Enviar Mensaje', "maxlength" : '500' ,'title':'Mensaje','required':True}),
		'avatar':widgets.HiddenInput(attrs={'title':'avatar','required':True,}),
		'Envio': widgets.HiddenInput(attrs={'title':'Usuario','required':True,}),
		'Actividad': widgets.HiddenInput(attrs={'title':'Actividad','required':True,}),
		'Recivio': widgets.HiddenInput(attrs={'title':'Actividad','required':True,}),
		'Estatus': widgets.HiddenInput(attrs={'required':True,'disabled':True}),
		}

class PeerToPeerForm(forms.ModelForm):
	class Meta:
		model = PeerToPeer
		fields = ('Mensaje','Envio','Recivio','Estatus','avatar')
		widgets = {
		'Mensaje': widgets.TextInput(attrs={"autofocus":True,"placeholder" : 'Enviar Mensaje', "maxlength" : '500' ,'title':'Mensaje','required':True}),
		'avatar':widgets.HiddenInput(attrs={'title':'avatar','required':True,}),
		'Envio': widgets.HiddenInput(attrs={'title':'Usuario','required':True,}),
		'Recivio': widgets.HiddenInput(attrs={'title':'mensaje','required':True,}),
		'Estatus': widgets.HiddenInput(attrs={'required':True,'disabled':True}),
		}