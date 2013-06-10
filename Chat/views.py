# Create your views here.
from datetime import date, datetime
from django.http import HttpResponse,HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from ControlActividades.forms import *
from Chat.forms import *
from django.template.context import RequestContext
from ControlActividades.models import *
from django.contrib.auth.models import User
from Usuarios.models import *
from Chat.models import *
from itertools import chain #para unir dos diccionarios
from django.contrib.auth.forms import UserCreationForm,  AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate, logout 
from django.contrib.auth.decorators import login_required
try: import simplejson as json
except ImportError: import json
from django.core import serializers
from django.db.models import Q


@login_required(login_url='/ingresar')
def Chat(request):
	usuario = request.user
	getperfil=Perfil.objects.get(user=usuario.id)
	mensajes = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).order_by("Fecha")
    	contador = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).count()
        Mensajes = Mensajeria.objects.filter(Recivio=usuario.id,Estatus=False).order_by('-id')[:1]
        Correo = CorreoForm();
    	return render_to_response('Chat/index.html', locals(), context_instance=RequestContext(request,{'email':Correo,'inbox':Mensajes,'perfilUer':getperfil,'login': usuario,'notificacion':mensajes,'numberRegister':contador}))

@login_required(login_url='/ingresar')
def Mensaje(request,id_Usuario):
    usuario = request.user
    getperfil=Perfil.objects.get(user=usuario.id)
    getusuarios=Perfil.objects.all()
    userGet = User.objects.get(pk=id_Usuario)
    mensajes = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).order_by("Fecha")
    contador = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).count()
    query1 = PeerToPeer.objects.filter(Envio=usuario.id,Recivio=id_Usuario,Estatus=False).order_by('id')
    query2 = PeerToPeer.objects.filter(Envio=id_Usuario,Recivio=usuario.id,Estatus=False).order_by('id')
    Mensajes = query1 | query2
    Correo = PeerToPeerForm();
    return render_to_response('Chat/peertopeer.html', locals(), context_instance=RequestContext(request,{"Recivio":userGet,'usuarios':getusuarios,'formulario':Correo,'inbox':Mensajes,'perfilUer':getperfil,'login': usuario,'notificacion':mensajes,'numberRegister':contador}))

@login_required(login_url='/ingresar')
def NuevaNotificacion(request,id_Actividad):
    usuario = request.user
    getperfil=Perfil.objects.get(user=usuario.id)
    getusuarios=Perfil.objects.all()
    mensajes = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).order_by("Fecha")
    contador = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).count()
    Mensajes = Mensajeria.objects.filter(Actividad=id_Actividad).order_by("Fecha")
    Actividades = Actividad.objects.get(pk=id_Actividad)
    Correo = CorreoForm();
    return render_to_response('Chat/Notificar.html', locals(), context_instance=RequestContext(request,{'usuarios':getusuarios,'Actividad':Actividades,'formulario':Correo,'inbox':Mensajes,'perfilUer':getperfil,'login': usuario,'notificacion':mensajes,'numberRegister':contador}))

@login_required(login_url='/ingresar')
def ResponderNotificacion(request,id_Actividad,id_Usuario):
    usuario = request.user
    getperfil=Perfil.objects.get(user=usuario.id)
    mensajes = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).order_by("Fecha")
    contador = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).count()
    Mensajes = Mensajeria.objects.filter(Actividad=id_Actividad).order_by("Fecha")
    Actividades = Actividad.objects.get(pk=id_Actividad)
    Correo = CorreoForm();
    return render_to_response('Chat/Responder.html', locals(), context_instance=RequestContext(request,{"Envio":id_Usuario,'Actividad':Actividades,'formulario':Correo,'inbox':Mensajes,'perfilUer':getperfil,'login': usuario,'notificacion':mensajes,'numberRegister':contador}))


@login_required(login_url='/ingresar')
def Correo(request):
    usuario = request.user
    if request.is_ajax() and request.method == 'POST':
        formulario = CorreoForm(request.POST)
        errores = ''
        datos = ''
        exito = False
        if formulario.is_valid():
            mensaje = Notificaciones()
            mensaje.Descripcion = request.POST['Mensaje']
            mensaje.Tipo = 'Mensaje'
            user = User.objects.get(pk=request.POST['Recivio'])
            mensaje.Usuario = user
            mensaje.Envio = usuario.username
            mensaje.save()
            formulario.save()
            exito = True
            datos = request.POST['Mensaje']
        else:
            errores = formulario.errors
        response = {'exito':exito,'date':datos,'errores':errores,}
        return HttpResponse(json.dumps(response), mimetype="application/json")
    else:
        raise Http404

@login_required(login_url='/ingresar')
def MensajeAjax(request):
    usuario = request.user
    if request.is_ajax() and request.method == 'POST':
        formulario = PeerToPeerForm(request.POST)
        errores = ''
        datos = ''
        exito = False
        if formulario.is_valid():
            formulario.save()
            exito = True
            datos = request.POST['Mensaje']
        else:
            errores = formulario.errors
        response = {'exito':exito,'date':datos,'errores':errores,}
        return HttpResponse(json.dumps(response), mimetype="application/json")
    else:
        raise Http404

@login_required(login_url='/ingresar')
def leidos(request):
    usuario = request.user
    if request.is_ajax() and request.method == 'POST':
        mensajes = Mensajeria.objects.filter(Actividad=request.POST['idActividad'])
        errores = ''
        exito = False
        for notificacion in mensajes:
            notificacion.Estatus=True
            notificacion.save()
            exito = True
        response = {'exito':exito,'errores':errores}
        return HttpResponse(json.dumps(response), mimetype="application/json")
    else:
        raise Http404