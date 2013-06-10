# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.template.loader import get_template
from django.template import Context
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.context import RequestContext
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm,  AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate, logout 
from django.contrib.auth.decorators import login_required
from Apps.forms import *
from ControlActividades.models import *
from Usuarios.models import *
try: import simplejson as json
except ImportError: import json


def Apps(request):
	login = request.user
	Apps = Aplicaciones.objects.all()
	return render_to_response('Apps/AppsPublica.html', context_instance=RequestContext(request,{'Apps':Apps,'login':login}))

@login_required(login_url='/ingresar')
def Appsprivada(request):
	login = request.user
	getperfil=Perfil.objects.get(user=login.id)
	Apps = Aplicaciones.objects.all()
	mensajes = Notificaciones.objects.filter(Estatus=False,Usuario=login.id).order_by("-Fecha")
    	contador = Notificaciones.objects.filter(Estatus=False,Usuario=login.id).count()
	return render_to_response('Apps/Apps.html', context_instance=RequestContext(request,{'perfilUer':getperfil,'login':login,'notificacion':mensajes,'numberRegister':contador,'Apps':Apps}))

@login_required(login_url='/ingresar')
def AgregarAplicacion(request):
	login = request.user
	getperfil=Perfil.objects.get(user=login.id)
	if request.user.is_authenticated():
		if request.method == "POST":
			formulario = AplicacionesForm(request.POST, request.FILES)
			if formulario.is_valid():
				formulario.save()
				return HttpResponseRedirect("/Apps")
		else:
			formulario = AplicacionesForm()
			mensajes = Notificaciones.objects.filter(Estatus=False,Usuario=login.id).order_by("-Fecha")
        		contador = Notificaciones.objects.filter(Estatus=False,Usuario=login.id).count()
			formulario.fields['desarrolador'].queryset = User.objects.filter(pk=request.user.id)
		return render_to_response('Apps/NuevaAplicacion.html',{'perfilUer':getperfil,'notificacion':mensajes,'numberRegister':contador,'formulario':formulario,'login':login}, context_instance=RequestContext(request))


