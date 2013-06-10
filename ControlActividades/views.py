# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from ControlActividades.forms import *
from django.template.context import RequestContext
from ControlActividades.models import *
from Usuarios.models import *
from django.contrib.auth.models import User
from itertools import chain #para unir dos diccionarios
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm,  AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate, logout 
from django.contrib.auth.decorators import login_required
try: import simplejson as json
except ImportError: import json
from django.core import serializers

@login_required(login_url='/ingresar')
def filter(request):
    usuario= request.user
    getperfil=Perfil.objects.get(user=usuario.id)
    formulario = ProyectosForm()
    mensajes = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).order_by("Fecha")
    contador = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).count()
    if usuario.is_staff:
        alluser= User.objects.all()
        Proyecto= Proyectos.objects.filter(Usuario=request.POST['usuario']).order_by('Proyecto')
        return render_to_response('ControlActividades/GestionProyectos.html', context_instance=RequestContext(request,{'perfilUer':getperfil,'allusers':alluser,'login': usuario,'notificacion':mensajes,'numberRegister':contador,'formulario':formulario,'Proyectos': Proyecto}))

@login_required(login_url='/ingresar')
def ControlActividades(request):
    usuario= request.user
    getperfil=Perfil.objects.get(user=usuario.id)
    formulario = ProyectosForm()
    mensajes = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).order_by("Fecha")
    contador = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).count()
    if usuario.is_staff:
        alluser= User.objects.all()
        Proyecto= Proyectos.objects.all().order_by('Proyecto')
        return render_to_response('ControlActividades/GestionProyectos.html', context_instance=RequestContext(request,{'perfilUer':getperfil,'allusers':alluser,'login': usuario,'notificacion':mensajes,'numberRegister':contador,'formulario':formulario,'Proyectos': Proyecto}))
    else:
        Proyecto = Proyectos.objects.filter(Usuario=usuario.id)
	return render_to_response('ControlActividades/GestionProyectos.html', context_instance=RequestContext(request,{'perfilUer':getperfil,'login': usuario,'notificacion':mensajes,'numberRegister':contador,'formulario':formulario,'Proyectos': Proyecto}))

@login_required(login_url='/ingresar')
def AgregarProyecto(request):
    usuario= request.user
    getperfil=Perfil.objects.get(user=usuario.id)
    if usuario.is_staff:
        mensajes = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).order_by("Fecha")
        contador = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).count()
        formulario = ProyectosForm()
        return render_to_response('ControlActividades/NuevoProyecto.html', context_instance=RequestContext(request,{'perfilUer':getperfil,'login': usuario,'notificacion':mensajes,'numberRegister':contador,'formulario':formulario}))
    

@login_required(login_url='/ingresar')
def AgregarProyectoAjax(request):
    usuario= request.user
    if request.is_ajax() and request.method == 'POST':
        formulario = ProyectosForm(request.POST)
        errores = ''
        datos = ''
        exito = False
        if formulario.is_valid():
            mensaje = Notificaciones()
            mensaje.Descripcion = request.POST['Proyecto']
            mensaje.Tipo = 'Proyecto'
            user = User.objects.get(pk=request.POST['Usuario'])
            mensaje.Usuario = user
            mensaje.Envio = usuario.username
            mensaje.save()
            formulario.save()
            exito = True
        else:
            errores = formulario.errors
        response = {'exito':exito,'errores':errores,}
        return HttpResponse(json.dumps(response), mimetype="application/json")
    else:
        raise Http404

@login_required(login_url='/ingresar')
def GetDataProyectoJson(request,id_proyecto):
    if request.is_ajax() and request.method == 'POST':
        data = serializers.serialize("json",Proyectos.objects.filter(pk=id_proyecto))
        return HttpResponse(data, mimetype="application/json")
    else:
        raise Http404

@login_required(login_url='/ingresar')
def GetDataProyectoJsonLast(request):
    if request.is_ajax() and request.method == 'POST':
        data = serializers.serialize("json",Proyectos.objects.filter().order_by('-id')[:1])
        return HttpResponse(data, mimetype="application/json")
    else:
        raise Http404

@login_required(login_url='/ingresar')
def EditarProyectoAjax(request,id_proyecto):
    if request.is_ajax() and request.method == 'POST':
        proyecto = Proyectos.objects.get(pk=id_proyecto)
        formulario = ProyectosForm(request.POST, instance=proyecto)
        errores = ''
        exito = False
        if formulario.is_valid():
            formulario.save()
            exito = True
        else:
            errores = formulario.errors
        response = {'exito':exito,'errores':errores}
        return HttpResponse(json.dumps(response), mimetype="application/json")
    else:
        raise Http404
        
@login_required(login_url='/ingresar')
def eliminarAjax(request,id_proyecto):
    if request.user.is_authenticated():
        if request.is_ajax() and request.method == 'POST':
            proyecto = Proyectos.objects.get(pk=id_proyecto)
            actividades = Actividad.objects.filter(Proyecto=id_proyecto)
            if(len(actividades)==0):  # Preguntamos por la longitud de la variable.
                proyecto.delete()
                exito = True
                errores = ''
            else:
                for activity in actividades:
                    avances = Avances.objects.filter(Actividad=activity.id)
                    if(len(avances)==0):  # Preguntamos por la longitud de la variable.
                        exito = True
                        errores = ''
                    else:
                        avances.delete()
                actividades.delete()
                proyecto.delete()
                exito = True
                errores = ''
            response = {'exito':exito,'errores':errores}
            return HttpResponse(json.dumps(response), mimetype="application/json")
        else:
            raise Http404

@login_required(login_url='/ingresar')
def Actividades(request,id_proyecto):
    usuario = request.user
    getperfil=Perfil.objects.get(user=usuario.id)
    formulario = CancelacionForm()
    formulario.fields['Usuario'].queryset = User.objects.filter(pk=usuario.id)
    Actividades = Actividad.objects.filter(Proyecto=id_proyecto,Finalizado=False).order_by("Actividad")
    mensajes = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).order_by("Fecha")
    contador = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).count()
    last=[]
    for ultimo in Actividades:
        lista=Avances.objects.filter(Actividad = ultimo.id ).order_by('-id')[:1]
        if(len(lista)==0):  # Preguntamos por la longitud de la variable.
            last.append(1)
        else:
            last.append(lista[0])
    return render_to_response('ControlActividades/Actividades.html',{'perfilUer':getperfil,'formulario':formulario,'notificacion':mensajes,'numberRegister':contador,'Actividades':Actividades,'login': usuario,'id_proyecto':id_proyecto,'porcentaje':last,}, context_instance=RequestContext(request))
    
@login_required(login_url='/ingresar')
def GetDataActividadJson(request,id_Actividad):
    if request.is_ajax() and request.method == 'POST':
        data = serializers.serialize("json",Actividad.objects.filter(pk=id_Actividad))
        return HttpResponse(data, mimetype="application/json")
    else:
        raise Http404

@login_required(login_url='/ingresar')
def NuevaActividad(request,id_proyecto):
    usuario= request.user
    getperfil=Perfil.objects.get(user=usuario.id)
    #if usuario.is_staff:
    formulario = ActividadForm()
    mensajes = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).order_by("Fecha")
    contador = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).count()
    formulario.fields['Proyecto'].queryset = Proyectos.objects.filter(id=id_proyecto)
    return render_to_response('ControlActividades/NuevaActividad.html', context_instance=RequestContext(request,{'perfilUer':getperfil,'login': usuario,'notificacion':mensajes,'numberRegister':contador,'formulario':formulario,}))

    
@login_required(login_url='/ingresar')
def NuevaActividadAjax(request):
    usuario= request.user
    if request.is_ajax() and request.method == 'POST':
        formulario = ActividadForm(request.POST)
        errores = ''
        exito = False
        if formulario.is_valid():
            mensaje = Notificaciones()
            mensaje.Descripcion = request.POST['Actividad']
            mensaje.Tipo = 'Actividad'
            user = User.objects.get(pk=request.POST['Usuario'])
            mensaje.Usuario = user
            mensaje.Envio = usuario.username
            mensaje.save()
            formulario.save()
            exito = True
        else:
            errores = formulario.errors
        response = {'exito':exito,'errores':errores}
        return HttpResponse(json.dumps(response), mimetype="application/json")
    else:
        raise Http404

@login_required(login_url='/ingresar')
def EditarAct(request,id_Actividad,id_proyecto):
    usuario= request.user
    getperfil=Perfil.objects.get(user=usuario.id)
    if  request.method == 'POST':
        actividad1 = Actividad.objects.get(pk=id_Actividad)
        formulario = ActividadForm(instance=actividad1)
        return render_to_response('ControlActividades/EditarActividad.html', context_instance=RequestContext(request,{'perfilUer':getperfil,'login': usuario,'formulario':formulario,}))
    else:
        actividad1 = Actividad.objects.get(pk=id_Actividad)
        formulario = ActividadForm(instance=actividad1)
        formulario.fields['Proyecto'].queryset = Proyectos.objects.filter(id=id_proyecto)
        mensajes = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).order_by("Fecha")
        contador = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).count()
        return render_to_response('ControlActividades/EditarActividad.html', context_instance=RequestContext(request,{'perfilUer':getperfil,'login': usuario,'notificacion':mensajes,'numberRegister':contador,'formulario':formulario,'id_Actividad':id_Actividad,}))

@login_required(login_url='/ingresar')
def EditarActAjax(request,id_Actividad):
    if request.is_ajax() and request.method == 'POST':
        actividad1 = Actividad.objects.get(pk=id_Actividad)
        formulario = ActividadForm(request.POST, instance=actividad1)
        errores = ''
        exito = False
        if formulario.is_valid():
            formulario.save()
            exito = True
        else:
            errores = formulario.errors
        response = {'exito':exito,'errores':errores,}
        return HttpResponse(json.dumps(response), mimetype="application/json")
    else:
        raise Http404


@login_required(login_url='/ingresar')
def finalizarActAjax(request,id_Actividad):
    if request.is_ajax() and request.method == 'POST':
        errores = ''
        exito = False
        if request.user.has_perm('ControlActividades.change_Actividad'):
            actividad = Actividad.objects.get(pk=id_Actividad)
            actividad.Finalizado=True
            actividad.Estatus=False
            actividad.Proceso=False
            actividad.save()
            exito = True
        response = {'exito':exito,'errores':errores}
        return HttpResponse(json.dumps(response), mimetype="application/json")
    else:
        raise Http404

@login_required(login_url='/ingresar')
def EliminarActAjax(request,id_Actividad):
    if request.is_ajax() and request.method == 'POST':
        if request.user.has_perm('ControlActividades.delete_Actividad'):
            formulario = CancelacionForm(request.POST)
            errores = ''
            exito = False
            formulario.actividad=request.POST['actividad']
            if formulario.is_valid():
                formulario.save()
                actividades = Actividad.objects.get(pk=id_Actividad)
                avances = Avances.objects.filter(Actividad=actividades.id)
                if(len(avances)==0):  # Preguntamos por la longitud de la variable.
                    actividades.delete()
                    exito=True
                else:
                    avances.delete()
                    actividades.delete()
                    exito = True
            else:
                errores = formulario.errors
            response = {'exito':exito,'errores':errores}
            return HttpResponse(json.dumps(response), mimetype="application/json")
        else:
            raise Http404

@login_required(login_url='/ingresar')
def Historial(request,id_Actividad,id_proyecto):
    usuario= request.user
    getperfil=Perfil.objects.get(user=usuario.id)
    mensajes = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).order_by("Fecha")
    contador = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).count()
    views= Avances.objects.filter(Actividad=id_Actividad).order_by('-id')
    formulario = AvancesForm()
    formulario.fields['Actividad'].queryset = Actividad.objects.filter(id=id_Actividad)
    ultimo=Avances.objects.filter(Actividad= id_Actividad ).order_by('-id')[:1]
    Activity = Actividad.objects.get(pk=id_Actividad)
    if(len(ultimo)==0):  # Preguntamos por la longitud de la variable.
        last=1
    else:
        last=ultimo[0].Points 
    return render_to_response('ControlActividades/Avances.html', context_instance=RequestContext(request,{'Activida':Activity,'perfilUer':getperfil,'Avance':views,'notificacion':mensajes,'numberRegister':contador,'id_Actividad':id_Actividad,'Avances':views,'login': usuario,'formulario':formulario,'id_proyecto':id_proyecto,'porcentaje':last,}))


@login_required(login_url='/ingresar')
def GetDataAvanceJsonLast(request):
    if request.is_ajax() and request.method == 'POST':
        data = serializers.serialize("json",Avances.objects.filter().order_by('-id')[:1])
        return HttpResponse(data, mimetype="application/json")
    else:
        raise Http404

@login_required(login_url='/ingresar')
def AgregarAvanceAjax(request):
    if request.is_ajax() and request.method == 'POST':
        formulario = AvancesForm(request.POST)
        errores = ''
        exito = False
        if formulario.is_valid():
            formulario.save()
            lista=Avances.objects.filter(Actividad = request.POST['Actividad'] ).order_by('-id')[:1]
            if(len(lista)==1):  # Preguntamos por la longitud de la variable.
                actividad = Actividad.objects.get(pk=request.POST['Actividad'])
                actividad.Proceso=True
                actividad.save()
            for ultimo in lista:      
                if ultimo.Points == 100:
                    actividad = Actividad.objects.get(pk=request.POST['Actividad'])
                    actividad.Proceso=False
                    actividad.Estatus=False
                    actividad.save()
            exito = True
        else:
            errores = formulario.errors
        response = {'exito':exito,'errores':errores}
        return HttpResponse(json.dumps(response), mimetype="application/json")
    else:
        raise Http404    
