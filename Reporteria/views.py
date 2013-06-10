# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.context import RequestContext
from ControlActividades.models import *
from Usuarios.models import *
from django.contrib.auth.models import User
from itertools import chain #para unir dos diccionarios
from datetime import date, datetime
from django.contrib.auth.forms import UserCreationForm,  AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate, logout 
from django.contrib.auth.decorators import login_required
try: import simplejson as json
except ImportError: import json
from django.core import serializers


@login_required(login_url='/ingresar')
def Reporteria(request):
    d = datetime.today()
    usuario = request.user
    if request.method == 'POST':
        persona= User.objects.all()
        status= request.POST['estatus']
        getuser = request.POST['usuario']
        start_date = request.POST['from']
        end_date = request.POST['to']
        if status == 'PENDIENTES':
            if getuser== '0':#TODOS
                if start_date =='' and end_date=='':
                    Actividades = Actividad.objects.filter(Estatus=True,Finalizado=False).order_by("-Fecha")
                    last=[]
                    for ultimo in Actividades:
                        lista=Avances.objects.filter(Actividad = ultimo.id ).order_by('-id')[:1]
                        if(len(lista)==0):  # Preguntamos por la longitud de la variable.
                            last.append(1)
                        else:
                            last.append(lista[0])
                    return render_to_response('Reporteria/reporteALL.html', context_instance=RequestContext(request,{'FechaActual':d,'Actividades': Actividades,'porcentaje':last,'Personal':persona}))   
                else:
                    Actividades = Actividad.objects.filter(Estatus=True,Finalizado=False,Desde__range=(start_date, end_date)).order_by("-Fecha")
                    last=[]
                    for ultimo in Actividades:
                        lista=Avances.objects.filter(Actividad = ultimo.id ).order_by('-id')[:1]
                        if(len(lista)==0):  # Preguntamos por la longitud de la variable.
                            last.append(1)
                        else:
                            last.append(lista[0])
                    return render_to_response('Reporteria/reporteALL.html', context_instance=RequestContext(request,{'FechaActual':d,'Actividades': Actividades,'porcentaje':last,'Personal':persona}))  
            else:
                persona= User.objects.get(pk=getuser)
                if start_date =='' and end_date=='':
                    Actividades = Actividad.objects.filter(Estatus=True,Finalizado=False,Usuario=getuser).order_by("-Fecha")
                    last=[]
                    for ultimo in Actividades:
                        lista=Avances.objects.filter(Actividad = ultimo.id ).order_by('-id')[:1]
                        if(len(lista)==0):  # Preguntamos por la longitud de la variable.
                            last.append(1)
                        else:
                            last.append(lista[0])
                    return render_to_response('Reporteria/ViewReporete.html', context_instance=RequestContext(request,{'FechaActual':d,'Actividades': Actividades,'porcentaje':last,'Personal':persona}))
                else:
                    Actividades = Actividad.objects.filter(Usuario=getuser,Estatus=True,Finalizado=False,Desde__range=(start_date, end_date)).order_by("-Fecha")
                    last=[]
                    for ultimo in Actividades:
                        lista=Avances.objects.filter(Actividad = ultimo.id ).order_by('-id')[:1]
                        if(len(lista)==0):  # Preguntamos por la longitud de la variable.
                            last.append(1)
                        else:
                            last.append(lista[0])
                    return render_to_response('Reporteria/ViewReporete.html', context_instance=RequestContext(request,{'FechaActual':d,'Actividades': Actividades,'porcentaje':last,'Personal':persona}))  

        if status == 'TERMINADAS':
            if getuser== '0':#TODOS
                if start_date =='' and end_date=='':
                    Actividades = Actividad.objects.filter(Estatus=False,Proceso=False,Finalizado=False).order_by("-Fecha")
                    last=[]
                    for ultimo in Actividades:
                        lista=Avances.objects.filter(Actividad = ultimo.id ).order_by('-id')[:1]
                        if(len(lista)==0):  # Preguntamos por la longitud de la variable.
                            last.append(1)
                        else:
                            last.append(lista[0])
                    return render_to_response('Reporteria/reporteALL.html', context_instance=RequestContext(request,{'FechaActual':d,'Actividades': Actividades,'porcentaje':last,'Personal':persona}))   
                else:
                    Actividades = Actividad.objects.filter(Estatus=False,Proceso=False,Finalizado=False,Desde__range=(start_date, end_date)).order_by("-Fecha")
                    last=[]
                    for ultimo in Actividades:
                        lista=Avances.objects.filter(Actividad = ultimo.id ).order_by('-id')[:1]
                        if(len(lista)==0):  # Preguntamos por la longitud de la variable.
                            last.append(1)
                        else:
                            last.append(lista[0])
                    return render_to_response('Reporteria/reporteALL.html', context_instance=RequestContext(request,{'FechaActual':d,'Actividades': Actividades,'porcentaje':last,'Personal':persona}))   
            else:
                persona= User.objects.get(pk=getuser)
                if start_date =='' and end_date=='':
                    Actividades = Actividad.objects.filter(Usuario=getuser,Estatus=False,Proceso=False,Finalizado=False).order_by("-Fecha")
                    last=[]
                    for ultimo in Actividades:
                        lista=Avances.objects.filter(Actividad = ultimo.id ).order_by('-id')[:1]
                        if(len(lista)==0):  # Preguntamos por la longitud de la variable.
                            last.append(1)
                        else:
                            last.append(lista[0])
                    return render_to_response('Reporteria/ViewReporete.html', context_instance=RequestContext(request,{'FechaActual':d,'Actividades': Actividades,'porcentaje':last,'Personal':persona}))
                else:
                    Actividades = Actividad.objects.filter(Usuario=getuser,Estatus=False,Proceso=False,Finalizado=False,Desde__range=(start_date, end_date)).order_by("-Fecha")
                    last=[]
                    for ultimo in Actividades:
                        lista=Avances.objects.filter(Actividad = ultimo.id ).order_by('-id')[:1]
                        if(len(lista)==0):  # Preguntamos por la longitud de la variable.
                            last.append(1)
                        else:
                            last.append(lista[0])
                    return render_to_response('Reporteria/ViewReporete.html', context_instance=RequestContext(request,{'FechaActual':d,'Actividades': Actividades,'porcentaje':last,'Personal':persona}))   


        if status == 'FINALIZADAS':
            if getuser== '0':#TODOS
                if start_date =='' and end_date=='':
                    Actividades = Actividad.objects.filter(Finalizado=True).order_by("-Fecha")
                    last=[]
                    for ultimo in Actividades:
                        lista=Avances.objects.filter(Actividad = ultimo.id ).order_by('-id')[:1]
                        if(len(lista)==0):  # Preguntamos por la longitud de la variable.
                            last.append(1)
                        else:
                            last.append(lista[0])
                    return render_to_response('Reporteria/reporteALL.html', context_instance=RequestContext(request,{'FechaActual':d,'Actividades': Actividades,'porcentaje':last,'Personal':persona}))   
                else:
                    Actividades = Actividad.objects.filter(Finalizado=True,Desde__range=(start_date, end_date)).order_by("-Fecha")
                    last=[]
                    for ultimo in Actividades:
                        lista=Avances.objects.filter(Actividad = ultimo.id ).order_by('-id')[:1]
                        if(len(lista)==0):  # Preguntamos por la longitud de la variable.
                            last.append(1)
                        else:
                            last.append(lista[0])
                    return render_to_response('Reporteria/reporteALL.html', context_instance=RequestContext(request,{'FechaActual':d,'Actividades': Actividades,'porcentaje':last,'Personal':persona}))   
            else:
                persona= User.objects.get(pk=getuser)
                if start_date =='' and end_date=='':
                    Actividades = Actividad.objects.filter(Usuario=getuser,Finalizado=True).order_by("-Fecha")
                    last=[]
                    for ultimo in Actividades:
                        lista=Avances.objects.filter(Actividad = ultimo.id ).order_by('-id')[:1]
                        if(len(lista)==0):  # Preguntamos por la longitud de la variable.
                            last.append(1)
                        else:
                            last.append(lista[0])
                    return render_to_response('Reporteria/ViewReporete.html', context_instance=RequestContext(request,{'FechaActual':d,'Actividades': Actividades,'porcentaje':last,'Personal':persona}))   
                else:
                    Actividades = Actividad.objects.filter(Usuario=getuser,Finalizado=True,Desde__range=(start_date, end_date)).order_by("-Fecha")
                    last=[]
                    for ultimo in Actividades:
                        lista=Avances.objects.filter(Actividad = ultimo.id ).order_by('-id')[:1]
                        if(len(lista)==0):  # Preguntamos por la longitud de la variable.
                            last.append(1)
                        else:
                            last.append(lista[0])
                    return render_to_response('Reporteria/ViewReporete.html', context_instance=RequestContext(request,{'FechaActual':d,'Actividades': Actividades,'porcentaje':last,'Personal':persona}))   

        if status == 'ATRAZADAS':
            if getuser== '0':#TODOS
                if start_date =='' and end_date=='':
                    Actividades = Actividad.objects.filter(Estatus=True).order_by("-Fecha")
                    last=[]
                    for ultimo in Actividades:
                        lista=Avances.objects.filter(Actividad = ultimo.id ).order_by('-id')[:1]
                        if(len(lista)==0):  # Preguntamos por la longitud de la variable.
                            last.append(1)
                        else:
                            last.append(lista[0])
                    return render_to_response('Reporteria/reporteALL.html', context_instance=RequestContext(request,{'FechaActual':d,'Actividades': Actividades,'porcentaje':last,'Personal':persona}))   
                else:
                    Actividades = Actividad.objects.filter(Estatus=True,Desde__range=(start_date, end_date)).order_by("-Fecha")
                    last=[]
                    for ultimo in Actividades:
                        lista=Avances.objects.filter(Actividad = ultimo.id ).order_by('-id')[:1]
                        if(len(lista)==0):  # Preguntamos por la longitud de la variable.
                            last.append(1)
                        else:
                            last.append(lista[0])
                    return render_to_response('Reporteria/reporteALL.html', context_instance=RequestContext(request,{'FechaActual':d,'Actividades': Actividades,'porcentaje':last,'Personal':persona}))   
            else:
                persona= User.objects.get(pk=getuser)
                if start_date =='' and end_date=='':
                    Actividades = Actividad.objects.filter(Usuario=getuser,Estatus=True).order_by("-Fecha")
                    last=[]
                    for ultimo in Actividades:
                        lista=Avances.objects.filter(Actividad = ultimo.id ).order_by('-id')[:1]
                        if(len(lista)==0):  # Preguntamos por la longitud de la variable.
                            last.append(1)
                        else:
                            last.append(lista[0])
                    return render_to_response('Reporteria/ViewReporete.html', context_instance=RequestContext(request,{'FechaActual':d,'Actividades': Actividades,'porcentaje':last,'Personal':persona}))   
                else:
                    Actividades = Actividad.objects.filter(Usuario=getuser,Estatus=True,Desde__range=(start_date, end_date)).order_by("-Fecha")
                    last=[]
                    for ultimo in Actividades:
                        lista=Avances.objects.filter(Actividad = ultimo.id ).order_by('-id')[:1]
                        if(len(lista)==0):  # Preguntamos por la longitud de la variable.
                            last.append(1)
                        else:
                            last.append(lista[0])
                    return render_to_response('Reporteria/ViewReporete.html', context_instance=RequestContext(request,{'FechaActual':d,'Actividades': Actividades,'porcentaje':last,'Personal':persona}))


        if status == 'TODAS':
            if getuser== '0':#TODOS
                if start_date =='' and end_date=='':
                    Actividades = Actividad.objects.all().order_by("-Fecha")
                    last=[]
                    for ultimo in Actividades:
                        lista=Avances.objects.filter(Actividad = ultimo.id ).order_by('-id')[:1]
                        if(len(lista)==0):  # Preguntamos por la longitud de la variable.
                            last.append(1)
                        else:
                            last.append(lista[0])
                    return render_to_response('Reporteria/reporteALL.html', context_instance=RequestContext(request,{'FechaActual':d,'Actividades': Actividades,'porcentaje':last,'Personal':persona}))   
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
                    return render_to_response('Reporteria/reporteALL.html', context_instance=RequestContext(request,{'FechaActual':d,'Actividades': Actividades,'porcentaje':last,'Personal':persona}))   
            else:
                persona= User.objects.get(pk=getuser)
                if start_date =='' and end_date=='':
                    Actividades = Actividad.objects.filter(Usuario=getuser).order_by("-Fecha")
                    last=[]
                    for ultimo in Actividades:
                        lista=Avances.objects.filter(Actividad = ultimo.id ).order_by('-id')[:1]
                        if(len(lista)==0):  # Preguntamos por la longitud de la variable.
                            last.append(1)
                        else:
                            last.append(lista[0])
                    return render_to_response('Reporteria/ViewReporete.html', context_instance=RequestContext(request,{'FechaActual':d,'Actividades': Actividades,'porcentaje':last,'Personal':persona}))   
                else:
                    Actividades = Actividad.objects.filter(Usuario=getuser,Desde__range=(start_date, end_date)).order_by("-Fecha")
                    last=[]
                    for ultimo in Actividades:
                        lista=Avances.objects.filter(Actividad = ultimo.id ).order_by('-id')[:1]
                        if(len(lista)==0):  # Preguntamos por la longitud de la variable.
                            last.append(1)
                        else:
                            last.append(lista[0])
                    return render_to_response('Reporteria/ViewReporete.html', context_instance=RequestContext(request,{'FechaActual':d,'Actividades': Actividades,'porcentaje':last,'Personal':persona}))   
    else:           
        usuario= request.user
        getperfil=Perfil.objects.get(user=usuario.id)
        alluser= User.objects.all()
        mensajes = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).order_by("Fecha")
        contador = Notificaciones.objects.filter(Estatus=False,Usuario=usuario.id).count()
        return render_to_response('Reporteria/reportes.html', context_instance=RequestContext(request,{'perfilUer':getperfil,'allusers':alluser,'login': usuario,'notificacion':mensajes,'numberRegister':contador}))
