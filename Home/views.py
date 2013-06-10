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

@login_required(login_url='/ingresar')
def Principal(request):
    usuario = request.user
    getperfil=Perfil.objects.get(user=usuario.id)
    d = date.today()
    if usuario.is_staff:
        formulario = CancelacionForm()
        Correo = CorreoForm();
        alluser= User.objects.all()
        formulario.fields['Usuario'].queryset = User.objects.filter(pk=usuario.id)
        Actividades = Actividad.objects.filter(Estatus=True,Finalizado=False).order_by("-Fecha")
        mensajes = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).order_by("-Fecha")
        contador = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).count()
        last=[]
        for ultimo in Actividades:
            lista=Avances.objects.filter(Actividad = ultimo.id ).order_by('-id')[:1]
            if(len(lista)==0):  # Preguntamos por la longitud de la variable.
                last.append(1)
            else:
                last.append(lista[0])
        return render_to_response('HOME/home.html',{'email':Correo,'perfilUer':getperfil,'allusers':alluser,'FechaActual':d,'Actividades':Actividades,'notificacion':mensajes,'numberRegister':contador,'login': usuario,'formulario':formulario,'porcentaje':last,}, context_instance=RequestContext(request))   
    else:
        Actividades = Actividad.objects.filter(Estatus=True,Finalizado=False,Usuario=usuario). order_by("-Fecha")
        mensajes = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).order_by("-Fecha")
        contador = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).count()
        last=[]
        for ultimo in Actividades:
            lista=Avances.objects.filter(Actividad = ultimo.id ).order_by('-id')[:1]
            if(len(lista)==0):  # Preguntamos por la longitud de la variable.
                last.append(1)
            else:
                last.append(lista[0])
        return render_to_response('HOME/home.html',{'perfilUer':getperfil,'FechaActual':d,'Actividades':Actividades,'login': usuario,'notificacion':mensajes,'numberRegister':contador,'porcentaje':last,}, context_instance=RequestContext(request))   


@login_required(login_url='/ingresar')
def addActividades(request,id_Actividad):
    usuario= request.user
    getperfil=Perfil.objects.get(user=usuario.id)
    views= Avances.objects.filter(Actividad=id_Actividad).order_by('-id')
    formulario = AvancesForm()
    mensajes = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).order_by("-Fecha")
    contador = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).count()
    formulario.fields['Actividad'].queryset = Actividad.objects.filter(id=id_Actividad)
    ultimo=Avances.objects.filter(Actividad= id_Actividad ).order_by('-id')[:1]
    if(len(ultimo)==0):  # Preguntamos por la longitud de la variable.
        last=1
    else:
        last=ultimo[0].Points
    return render_to_response('HOME/AddAvances.html', context_instance=RequestContext(request,{'perfilUer':getperfil,'Avance':views,'id_Actividad':id_Actividad,'notificacion':mensajes,'numberRegister':contador,'Avances':views,'login': usuario,'formulario':formulario,'porcentaje':last,}))
    

@login_required(login_url='/ingresar')
def search(request):
    usuario = request.user
    getperfil=Perfil.objects.get(user=usuario.id)
    d = date.today()
    if usuario.is_staff:
        formulario = CancelacionForm()
        alluser= User.objects.all()
        status= request.POST['estatus']
        getuser = request.POST['usuario']
        start_date = request.POST['from']
        end_date = request.POST['to']
        if status == 'PENDIENTES':
            if getuser== '0':#TODOS
                if start_date =='' and end_date=='':
                    formulario.fields['Usuario'].queryset = User.objects.filter(pk=usuario.id)
                    Actividades = Actividad.objects.filter(Estatus=True,Finalizado=False).order_by("-Fecha")
                    mensajes = Notificaciones.objects.filter(Estatus=True,Usuario=usuario.id).order_by("-Fecha")
                    contador = Notificaciones.objects.filter(Estatus=True,Usuario=usuario.id).count()
                    last=[]
                    for ultimo in Actividades:
                        lista=Avances.objects.filter(Actividad = ultimo.id ).order_by('-id')[:1]
                        if(len(lista)==0):  # Preguntamos por la longitud de la variable.
                            last.append(1)
                        else:
                            last.append(lista[0])
                    return render_to_response('HOME/home.html',{'perfilUer':getperfil,'allusers':alluser,'FechaActual':d,'Actividades':Actividades,'notificacion':mensajes,'numberRegister':contador,'login': usuario,'formulario':formulario,'porcentaje':last,}, context_instance=RequestContext(request))   
                else:
                    Actividades = Actividad.objects.filter(Estatus=True,Finalizado=False,Desde__range=(start_date, end_date)).order_by("-Fecha")
                    formulario.fields['Usuario'].queryset = User.objects.filter(pk=usuario.id)
                    mensajes = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).order_by("-Fecha")
                    contador = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).count()
                    last=[]
                    for ultimo in Actividades:
                        lista=Avances.objects.filter(Actividad = ultimo.id ).order_by('-id')[:1]
                        if(len(lista)==0):  # Preguntamos por la longitud de la variable.
                            last.append(1)
                        else:
                            last.append(lista[0])
                    return render_to_response('HOME/home.html',{'perfilUer':getperfil,'allusers':alluser,'FechaActual':d,'Actividades':Actividades,'notificacion':mensajes,'numberRegister':contador,'login': usuario,'formulario':formulario,'porcentaje':last,}, context_instance=RequestContext(request))   
            else:
                if start_date =='' and end_date=='':
                    formulario.fields['Usuario'].queryset = User.objects.filter(pk=usuario.id)
                    Actividades = Actividad.objects.filter(Estatus=True,Finalizado=False,Usuario=getuser).order_by("-Fecha")
                    mensajes = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).order_by("-Fecha")
                    contador = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).count()
                    last=[]
                    for ultimo in Actividades:
                        lista=Avances.objects.filter(Actividad = ultimo.id ).order_by('-id')[:1]
                        if(len(lista)==0):  # Preguntamos por la longitud de la variable.
                            last.append(1)
                        else:
                            last.append(lista[0])
                    return render_to_response('HOME/home.html',{'perfilUer':getperfil,'allusers':alluser,'FechaActual':d,'Actividades':Actividades,'notificacion':mensajes,'numberRegister':contador,'login': usuario,'formulario':formulario,'porcentaje':last,}, context_instance=RequestContext(request))   
                else:
                    Actividades = Actividad.objects.filter(Usuario=getuser,Estatus=True,Finalizado=False,Desde__range=(start_date, end_date)).order_by("-Fecha")
                    formulario.fields['Usuario'].queryset = User.objects.filter(pk=usuario.id)
                    mensajes = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).order_by("-Fecha")
                    contador = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).count()
                    last=[]
                    for ultimo in Actividades:
                        lista=Avances.objects.filter(Actividad = ultimo.id ).order_by('-id')[:1]
                        if(len(lista)==0):  # Preguntamos por la longitud de la variable.
                            last.append(1)
                        else:
                            last.append(lista[0])
                    return render_to_response('HOME/home.html',{'perfilUer':getperfil,'allusers':alluser,'FechaActual':d,'Actividades':Actividades,'notificacion':mensajes,'numberRegister':contador,'login': usuario,'formulario':formulario,'porcentaje':last,}, context_instance=RequestContext(request))  

        if status == 'TERMINADAS':
            if getuser== '0':#TODOS
                if start_date =='' and end_date=='':
                    formulario.fields['Usuario'].queryset = User.objects.filter(pk=usuario.id)
                    Actividades = Actividad.objects.filter(Estatus=False,Proceso=False,Finalizado=False).order_by("-Fecha")
                    mensajes = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).order_by("-Fecha")
                    contador = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).count()
                    last=[]
                    for ultimo in Actividades:
                        lista=Avances.objects.filter(Actividad = ultimo.id ).order_by('-id')[:1]
                        if(len(lista)==0):  # Preguntamos por la longitud de la variable.
                            last.append(1)
                        else:
                            last.append(lista[0])
                    return render_to_response('HOME/home.html',{'perfilUer':getperfil,'allusers':alluser,'FechaActual':d,'Actividades':Actividades,'notificacion':mensajes,'numberRegister':contador,'login': usuario,'formulario':formulario,'porcentaje':last,}, context_instance=RequestContext(request))   
                else:
                    Actividades = Actividad.objects.filter(Estatus=False,Proceso=False,Finalizado=False,Desde__range=(start_date, end_date)).order_by("-Fecha")
                    formulario.fields['Usuario'].queryset = User.objects.filter(pk=usuario.id)
                    mensajes = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).order_by("-Fecha")
                    contador = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).count()
                    last=[]
                    for ultimo in Actividades:
                        lista=Avances.objects.filter(Actividad = ultimo.id ).order_by('-id')[:1]
                        if(len(lista)==0):  # Preguntamos por la longitud de la variable.
                            last.append(1)
                        else:
                            last.append(lista[0])
                    return render_to_response('HOME/home.html',{'perfilUer':getperfil,'allusers':alluser,'FechaActual':d,'Actividades':Actividades,'notificacion':mensajes,'numberRegister':contador,'login': usuario,'formulario':formulario,'porcentaje':last,}, context_instance=RequestContext(request))   
            else:
                if start_date =='' and end_date=='':
                    formulario.fields['Usuario'].queryset = User.objects.filter(pk=usuario.id)
                    Actividades = Actividad.objects.filter(Usuario=getuser,Estatus=False,Proceso=False,Finalizado=False).order_by("-Fecha")
                    mensajes = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).order_by("-Fecha")
                    contador = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).count()
                    last=[]
                    for ultimo in Actividades:
                        lista=Avances.objects.filter(Actividad = ultimo.id ).order_by('-id')[:1]
                        if(len(lista)==0):  # Preguntamos por la longitud de la variable.
                            last.append(1)
                        else:
                            last.append(lista[0])
                    return render_to_response('HOME/home.html',{'perfilUer':getperfil,'allusers':alluser,'FechaActual':d,'Actividades':Actividades,'notificacion':mensajes,'numberRegister':contador,'login': usuario,'formulario':formulario,'porcentaje':last,}, context_instance=RequestContext(request))   
                else:
                    Actividades = Actividad.objects.filter(Usuario=getuser,Estatus=False,Proceso=False,Finalizado=False,Desde__range=(start_date, end_date)).order_by("-Fecha")
                    formulario.fields['Usuario'].queryset = User.objects.filter(pk=usuario.id)
                    mensajes = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).order_by("-Fecha")
                    contador = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).count()
                    last=[]
                    for ultimo in Actividades:
                        lista=Avances.objects.filter(Actividad = ultimo.id ).order_by('-id')[:1]
                        if(len(lista)==0):  # Preguntamos por la longitud de la variable.
                            last.append(1)
                        else:
                            last.append(lista[0])
                    return render_to_response('HOME/home.html',{'perfilUer':getperfil,'allusers':alluser,'FechaActual':d,'Actividades':Actividades,'notificacion':mensajes,'numberRegister':contador,'login': usuario,'formulario':formulario,'porcentaje':last,}, context_instance=RequestContext(request))   


        if status == 'FINALIZADAS':
            if getuser== '0':#TODOS
                if start_date =='' and end_date=='':
                    formulario.fields['Usuario'].queryset = User.objects.filter(pk=usuario.id)
                    Actividades = Actividad.objects.filter(Finalizado=True).order_by("-Fecha")
                    mensajes = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).order_by("-Fecha")
                    contador = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).count()
                    last=[]
                    for ultimo in Actividades:
                        lista=Avances.objects.filter(Actividad = ultimo.id ).order_by('-id')[:1]
                        if(len(lista)==0):  # Preguntamos por la longitud de la variable.
                            last.append(1)
                        else:
                            last.append(lista[0])
                    return render_to_response('HOME/home.html',{'perfilUer':getperfil,'allusers':alluser,'FechaActual':d,'Actividades':Actividades,'notificacion':mensajes,'numberRegister':contador,'login': usuario,'formulario':formulario,'porcentaje':last,}, context_instance=RequestContext(request))   
                else:
                    Actividades = Actividad.objects.filter(Finalizado=True,Desde__range=(start_date, end_date)).order_by("-Fecha")
                    formulario.fields['Usuario'].queryset = User.objects.filter(pk=usuario.id)
                    mensajes = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).order_by("-Fecha")
                    contador = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).count()
                    last=[]
                    for ultimo in Actividades:
                        lista=Avances.objects.filter(Actividad = ultimo.id ).order_by('-id')[:1]
                        if(len(lista)==0):  # Preguntamos por la longitud de la variable.
                            last.append(1)
                        else:
                            last.append(lista[0])
                    return render_to_response('HOME/home.html',{'perfilUer':getperfil,'allusers':alluser,'FechaActual':d,'Actividades':Actividades,'notificacion':mensajes,'numberRegister':contador,'login': usuario,'formulario':formulario,'porcentaje':last,}, context_instance=RequestContext(request))   
            else:
                if start_date =='' and end_date=='':
                    formulario.fields['Usuario'].queryset = User.objects.filter(pk=usuario.id)
                    Actividades = Actividad.objects.filter(Usuario=getuser,Finalizado=True).order_by("-Fecha")
                    mensajes = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).order_by("-Fecha")
                    contador = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).count()
                    last=[]
                    for ultimo in Actividades:
                        lista=Avances.objects.filter(Actividad = ultimo.id ).order_by('-id')[:1]
                        if(len(lista)==0):  # Preguntamos por la longitud de la variable.
                            last.append(1)
                        else:
                            last.append(lista[0])
                    return render_to_response('HOME/home.html',{'perfilUer':getperfil,'allusers':alluser,'FechaActual':d,'Actividades':Actividades,'notificacion':mensajes,'numberRegister':contador,'login': usuario,'formulario':formulario,'porcentaje':last,}, context_instance=RequestContext(request))   
                else:
                    Actividades = Actividad.objects.filter(Usuario=getuser,Finalizado=True,Desde__range=(start_date, end_date)).order_by("-Fecha")
                    formulario.fields['Usuario'].queryset = User.objects.filter(pk=usuario.id)
                    mensajes = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).order_by("-Fecha")
                    contador = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).count()
                    last=[]
                    for ultimo in Actividades:
                        lista=Avances.objects.filter(Actividad = ultimo.id ).order_by('-id')[:1]
                        if(len(lista)==0):  # Preguntamos por la longitud de la variable.
                            last.append(1)
                        else:
                            last.append(lista[0])
                    return render_to_response('HOME/home.html',{'perfilUer':getperfil,'allusers':alluser,'FechaActual':d,'Actividades':Actividades,'notificacion':mensajes,'numberRegister':contador,'login': usuario,'formulario':formulario,'porcentaje':last,}, context_instance=RequestContext(request))   

        if status == 'ATRAZADAS':
            if getuser== '0':#TODOS
                if start_date =='' and end_date=='':
                    formulario.fields['Usuario'].queryset = User.objects.filter(pk=usuario.id)
                    Actividades = Actividad.objects.filter(Estatus=True).order_by("-Fecha")
                    mensajes = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).order_by("-Fecha")
                    contador = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).count()
                    last=[]
                    for ultimo in Actividades:
                        lista=Avances.objects.filter(Actividad = ultimo.id ).order_by('-id')[:1]
                        if(len(lista)==0):  # Preguntamos por la longitud de la variable.
                            last.append(1)
                        else:
                            last.append(lista[0])
                    return render_to_response('HOME/home.html',{'perfilUer':getperfil,'allusers':alluser,'FechaActual':d,'Actividades':Actividades,'notificacion':mensajes,'numberRegister':contador,'login': usuario,'formulario':formulario,'porcentaje':last,}, context_instance=RequestContext(request))   
                else:
                    Actividades = Actividad.objects.filter(Estatus=True,Desde__range=(start_date, end_date)).order_by("-Fecha")
                    formulario.fields['Usuario'].queryset = User.objects.filter(pk=usuario.id)
                    mensajes = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).order_by("-Fecha")
                    contador = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).count()
                    last=[]
                    for ultimo in Actividades:
                        lista=Avances.objects.filter(Actividad = ultimo.id ).order_by('-id')[:1]
                        if(len(lista)==0):  # Preguntamos por la longitud de la variable.
                            last.append(1)
                        else:
                            last.append(lista[0])
                    return render_to_response('HOME/home.html',{'perfilUer':getperfil,'allusers':alluser,'FechaActual':d,'Actividades':Actividades,'notificacion':mensajes,'numberRegister':contador,'login': usuario,'formulario':formulario,'porcentaje':last,}, context_instance=RequestContext(request))   
            else:
                if start_date =='' and end_date=='':
                    formulario.fields['Usuario'].queryset = User.objects.filter(pk=usuario.id)
                    Actividades = Actividad.objects.filter(Usuario=getuser,Estatus=True).order_by("-Fecha")
                    mensajes = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).order_by("-Fecha")
                    contador = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).count()
                    last=[]
                    for ultimo in Actividades:
                        lista=Avances.objects.filter(Actividad = ultimo.id ).order_by('-id')[:1]
                        if(len(lista)==0):  # Preguntamos por la longitud de la variable.
                            last.append(1)
                        else:
                            last.append(lista[0])
                    return render_to_response('HOME/home.html',{'perfilUer':getperfil,'allusers':alluser,'FechaActual':d,'Actividades':Actividades,'notificacion':mensajes,'numberRegister':contador,'login': usuario,'formulario':formulario,'porcentaje':last,}, context_instance=RequestContext(request))   
                else:
                    Actividades = Actividad.objects.filter(Usuario=getuser,Estatus=True,Desde__range=(start_date, end_date)).order_by("-Fecha")
                    formulario.fields['Usuario'].queryset = User.objects.filter(pk=usuario.id)
                    mensajes = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).order_by("-Fecha")
                    contador = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).count()
                    last=[]
                    for ultimo in Actividades:
                        lista=Avances.objects.filter(Actividad = ultimo.id ).order_by('-id')[:1]
                        if(len(lista)==0):  # Preguntamos por la longitud de la variable.
                            last.append(1)
                        else:
                            last.append(lista[0])
                    return render_to_response('HOME/home.html',{'perfilUer':getperfil,'allusers':alluser,'FechaActual':d,'Actividades':Actividades,'notificacion':mensajes,'numberRegister':contador,'login': usuario,'formulario':formulario,'porcentaje':last,}, context_instance=RequestContext(request))   


        if status == 'TODAS':
            if getuser== '0':#TODOS
                if start_date =='' and end_date=='':
                    formulario.fields['Usuario'].queryset = User.objects.filter(pk=usuario.id)
                    Actividades = Actividad.objects.all().order_by("-Fecha")
                    mensajes = Notificaciones.objects.filter(Estatus=True,Usuario=usuario.id).order_by("-Fecha")
                    contador = Notificaciones.objects.filter(Estatus=True,Usuario=usuario.id).count()
                    last=[]
                    for ultimo in Actividades:
                        lista=Avances.objects.filter(Actividad = ultimo.id ).order_by('-id')[:1]
                        if(len(lista)==0):  # Preguntamos por la longitud de la variable.
                            last.append(1)
                        else:
                            last.append(lista[0])
                    return render_to_response('HOME/home.html',{'perfilUer':getperfil,'allusers':alluser,'FechaActual':d,'Actividades':Actividades,'notificacion':mensajes,'numberRegister':contador,'login': usuario,'formulario':formulario,'porcentaje':last,}, context_instance=RequestContext(request))   
                else:
                    Actividades = Actividad.objects.filter(Desde__range=(start_date, end_date)).order_by("-Fecha")
                    formulario.fields['Usuario'].queryset = User.objects.filter(pk=usuario.id)
                    #Actividades = Actividad.objects.filter(Usuario=request.POST['usuario']). order_by("-Fecha")
                    mensajes = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).order_by("-Fecha")
                    contador = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).count()
                    last=[]
                    for ultimo in Actividades:
                        lista=Avances.objects.filter(Actividad = ultimo.id ).order_by('-id')[:1]
                        if(len(lista)==0):  # Preguntamos por la longitud de la variable.
                            last.append(1)
                        else:
                            last.append(lista[0])
                    return render_to_response('HOME/home.html',{'perfilUer':getperfil,'allusers':alluser,'FechaActual':d,'Actividades':Actividades,'notificacion':mensajes,'numberRegister':contador,'login': usuario,'formulario':formulario,'porcentaje':last,}, context_instance=RequestContext(request))   
            else:
                if start_date =='' and end_date=='':
                    formulario.fields['Usuario'].queryset = User.objects.filter(pk=usuario.id)
                    Actividades = Actividad.objects.filter(Usuario=getuser).order_by("-Fecha")
                    mensajes = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).order_by("-Fecha")
                    contador = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).count()
                    last=[]
                    for ultimo in Actividades:
                        lista=Avances.objects.filter(Actividad = ultimo.id ).order_by('-id')[:1]
                        if(len(lista)==0):  # Preguntamos por la longitud de la variable.
                            last.append(1)
                        else:
                            last.append(lista[0])
                    return render_to_response('HOME/home.html',{'perfilUer':getperfil,'allusers':alluser,'FechaActual':d,'Actividades':Actividades,'notificacion':mensajes,'numberRegister':contador,'login': usuario,'formulario':formulario,'porcentaje':last,}, context_instance=RequestContext(request))   
                else:
                    Actividades = Actividad.objects.filter(Usuario=getuser,Desde__range=(start_date, end_date)).order_by("-Fecha")
                    formulario.fields['Usuario'].queryset = User.objects.filter(pk=usuario.id)
                    #Actividades = Actividad.objects.filter(Usuario=request.POST['usuario']). order_by("-Fecha")
                    mensajes = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).order_by("-Fecha")
                    contador = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).count()
                    last=[]
                    for ultimo in Actividades:
                        lista=Avances.objects.filter(Actividad = ultimo.id ).order_by('-id')[:1]
                        if(len(lista)==0):  # Preguntamos por la longitud de la variable.
                            last.append(1)
                        else:
                            last.append(lista[0])
                    return render_to_response('HOME/home.html',{'perfilUer':getperfil,'allusers':alluser,'FechaActual':d,'Actividades':Actividades,'notificacion':mensajes,'numberRegister':contador,'login': usuario,'formulario':formulario,'porcentaje':last,}, context_instance=RequestContext(request))   


@login_required(login_url='/ingresar')
def InBox(request):
    usuario = request.user
    if request.is_ajax() and request.method == 'POST':
        mensajes = Notificaciones.objects.filter(Usuario=usuario.id)
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

    