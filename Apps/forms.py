from django.forms import ModelForm,widgets
from django import forms
from Apps.models import *

class AplicacionesForm(forms.ModelForm):
	class Meta:
		model = Aplicaciones
		fields = ('desarrolador', 'titulo', 'descripcion','App')
		widgets = {
		'desarrolador': widgets.Select(attrs={"autofocus":True,"placeholder" : 'desarrolador', "maxlength" : '40' ,'title':'desarrolador','required':True}),
		'titulo': widgets.TextInput(attrs={"placeholder" : 'titulo','title':'titulo','required':True}),
		'descripcion': widgets.Textarea(attrs={"placeholder" : 'Descripcion','title':'descripcion','required':True}),
		}