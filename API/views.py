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
from ControlActividades.models import Notificaciones
from django.contrib.auth.forms import UserCreationForm,  AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate, logout 
from django.contrib.auth.decorators import login_required
from API.models import *
from Usuarios.models import *
try: import simplejson as json
except ImportError: import json

@login_required(login_url='/ingresar')
def CFDI(request):
	return render_to_response('CFDI/CFDI.html', context_instance=RequestContext(request,{}))

@login_required(login_url='/ingresar')
def desarrolladores(request):
	login=request.user
	getperfil=Perfil.objects.get(user=login.id)
	mensajes = Notificaciones.objects.filter(Estatus=False,Usuario=login.id).order_by("Fecha")
    	contador = Notificaciones.objects.filter(Estatus=False,Usuario=login.id).count()
	return render_to_response('API/developer.html', context_instance=RequestContext(request,{'perfilUer':getperfil,'login':login,'notificacion':mensajes,'numberRegister':contador,}))