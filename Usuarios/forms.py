from django.forms import widgets
from django import forms
from Usuarios.models import *
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email','is_staff','is_active','is_superuser','groups')
        widgets = {
		'username': widgets.TextInput(attrs={"autofocus":True,"placeholder" : 'Usuario', "maxlength" : '40' ,'title':'Usuario','required':True}),
		'first_name': widgets.TextInput(attrs={"placeholder" : 'Nombre','title':'Nombre'}),
		'last_name': widgets.TextInput(attrs={'title':'Apellido',"placeholder" : 'Apellido'}),
		'email': widgets.TextInput(attrs={'title':'Email',"placeholder" : 'Correo Electronico','required':True}),
		}

class UserFormPerfil(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
       
