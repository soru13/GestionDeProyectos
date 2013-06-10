# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.context import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,  AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate, logout 
from django.contrib.auth.decorators import login_required
from ControlActividades.models import *
from Usuarios.models import *
try: import simplejson as json
except ImportError: import json
from django.core import serializers
import datetime
import qsstats


@login_required(login_url='/ingresar')
def statistics(request):
	usuario = request.user
        getperfil=Perfil.objects.get(user=usuario.id)
	mensajes = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).order_by("Fecha")
    	contador = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).count()
	actividad = Actividad.objects.filter(Usuario=usuario.id).count()
	proyecto = Proyectos.objects.filter(Usuario=usuario.id).count()
	cancelacion = Cancelacion.objects.filter(Usuario=usuario.id).count()
	GOOGLE_API_KEY = 'clave'
    	qs = Actividad.objects.filter(Usuario=usuario.id)
    	qss = qsstats.QuerySetStats(qs, 'Fecha')
    	hoy = datetime.date.today()
    	hace_2_semanas = hoy - datetime.timedelta(weeks=2)
    	users_stats = qss.time_series(hace_2_semanas, hoy)
    	return render_to_response('statistics/index.html', locals(), context_instance=RequestContext(request,{'perfilUer':getperfil,'login': usuario,'notificacion':mensajes,'numberRegister':contador,'actividades':actividad,'proyectos':proyecto,'cancelaciones':cancelacion}))
    