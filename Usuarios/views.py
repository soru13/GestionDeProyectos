# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader
from Usuarios.forms import *
from django.template.context import RequestContext
from Usuarios.models import *
from ControlActividades.models import Notificaciones
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm,  AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate, logout 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group, Permission
try: import simplejson as json
except ImportError: import json



def ingresar(request):
    if not request.user.is_anonymous():
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        formulario = AuthenticationForm(request.POST)
        if formulario.is_valid:
            usuario = request.POST['username']
            clave = request.POST['password']
            acceso = authenticate(username=usuario, password=clave)
            if acceso is not None:
                if acceso.is_active:
                    if acceso.is_staff:
                        auth_login(request, acceso)
                        return HttpResponseRedirect('/')
                    else:
                        auth_login(request, acceso)
                        return HttpResponseRedirect('/')
                else:
                    return render_to_response('usuarios/noactivo.html', context_instance=RequestContext(request))
            else:
                return render_to_response('usuarios/nousuario.html', context_instance=RequestContext(request))
        else:
            return render_to_response('usuarios/noactivo.html', context_instance=RequestContext(request))
    else:
        formulario = AuthenticationForm()
	return render_to_response('usuarios/ingresar.html', context_instance=RequestContext(request,{'formulario': formulario}))

@login_required(login_url='/ingresar')
def usuarios(request):
    if request.user.is_authenticated():
        if request.user.is_staff:
            mensajes = Notificaciones.objects.filter(Estatus=False,Usuario=request.user.id).order_by("-Fecha")
            contador = Notificaciones.objects.filter(Estatus=False,Usuario=request.user.id).count()
            login=request.user
            getperfil=Perfil.objects.get(user=login.id)
            usuarios = User.objects.all()
            return render_to_response('usuarios/usuarios.html', context_instance=RequestContext(request,{'perfilUer':getperfil,'notificacion':mensajes,'numberRegister':contador,'usuarios': usuarios,'login':login}))
        else:
            return HttpResponseRedirect('/Apps')

@login_required(login_url='/ingresar')
def NuevoUsuario(request):
    login=request.user
    getperfil=Perfil.objects.get(user=login.id)
    mensajes = Notificaciones.objects.filter(Estatus=False,Usuario=login.id).order_by("-Fecha")
    contador = Notificaciones.objects.filter(Estatus=False,Usuario=login.id).count()
    formulario = UserCreationForm()
    return render_to_response('usuarios/NuevoUsuario.html',{'perfilUer':getperfil,'notificacion':mensajes,'numberRegister':contador,'formulario':formulario,'login':login}, context_instance=RequestContext(request))


def AgregarUsuarioAjax(request):
    if request.is_ajax() and request.method == 'POST':
        formulario = UserCreationForm(request.POST)
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
def EditarPerfil(request,id_usuario):
    if request.user.is_staff:
        login=request.user
        user = User.objects.get(pk=id_usuario)
        mensajes = Notificaciones.objects.filter(Estatus=False,Usuario=login.id).order_by("-Fecha")
        contador = Notificaciones.objects.filter(Estatus=False,Usuario=login.id).count()
        # formulario inicial
        user_form = UserForm(instance=user)
        return render_to_response('usuarios/editar_perfil.html', {'notificacion':mensajes,'numberRegister':contador, 'user_form': user_form,'login':login}, context_instance=RequestContext(request))
    else:
        raise Http404

@login_required(login_url='/ingresar')
def EditarUsuarioAjax(request):
    if request.is_ajax() and request.method == 'POST':
        usuario = User.objects.get(pk=request.POST['id_usuario'])
        formulario = UserForm(request.POST, instance=usuario)
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
def EditarPerfilLogin(request):
    login=request.user
    mensajes = Notificaciones.objects.filter(Estatus=False,Usuario=login.id).order_by("-Fecha")
    contador = Notificaciones.objects.filter(Estatus=False,Usuario=login.id).count()
    if request.method == 'POST':
        # formulario enviado
        user_form = UserFormPerfil(request.POST,request.FILES,instance=request.user)
        perfil = PerfilForm(request.POST,request.FILES,instance=request.user.perfil)
        if user_form.is_valid() and perfil.is_valid():
            # formulario validado correctamente
            user_form.save()
            perfil.save()
            return HttpResponseRedirect('/')
    else:
        # formulario inicial
        user_form = UserFormPerfil(instance=request.user)
        perfil = PerfilForm(instance=request.user.perfil)
        perfil.fields['user'].queryset = User.objects.filter(pk=request.user.id)
    return render_to_response('usuarios/PerfilUsuario.html', {'perfil_form':perfil,'notificacion':mensajes,'numberRegister':contador, 'user_form': user_form,'login':login }, context_instance=RequestContext(request))



@login_required(login_url='/ingresar')
def resetPassword(request):
    login=request.user
    mensajes = Notificaciones.objects.filter(Estatus=False,Usuario=login.id).order_by("-Fecha")
    contador = Notificaciones.objects.filter(Estatus=False,Usuario=login.id).count()
    if request.POST:
        password = request.POST['password'].encode('ascii','replace')
        confirm_password = request.POST['confirm_password'].encode('ascii','replace')
        if password == confirm_password:
            login.set_password(confirm_password)
            login.save()
            return HttpResponseRedirect('/')
        else:
            raise Http404
    else:
        return render_to_response('usuarios/reset.html', {'notificacion':mensajes,'numberRegister':contador,'login':login }, context_instance=RequestContext(request))



@login_required(login_url='/ingresar')
def CrearPerfil(request):
    login=request.user
    if request.method == 'POST':
        # formulario enviado
        user_form = PerfilForm(request.POST,request.FILES)
        #perfil_form = PerfilForm(request.POST, instance=request.user.perfil)

        if user_form.is_valid():
            # formulario validado correctamente
            user_form.save()
            #perfil_form.save()
            return HttpResponseRedirect('/')

    else:
        # formulario inicial
        user = User.objects.get(pk=login.id)
        user_form = PerfilForm(instance=user.perfil)
        user_form.fields['user'].queryset = User.objects.filter(pk=login.id)
        #perfil_form = PerfilForm(instance=request.user.perfil)

    return render_to_response('usuarios/PerfilUsuario.html', { 'user_form': user_form,'login':login }, context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def eliminar(request,id_usuario):
    usuario = User.objects.get(pk=id_usuario)
    usuario.delete()
    return HttpResponseRedirect("/Usuarios")

@login_required(login_url='/ingresar')
def cerrar(request):
    logout(request)
    return HttpResponseRedirect('/ingresar')