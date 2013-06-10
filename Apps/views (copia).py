# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.template.loader import get_template
from django.template import Context
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.context import RequestContext
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm,  AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate, logout 
from django.contrib.auth.decorators import login_required
#from Apps.models import Datos
#from Apps.forms import UsuariosForm
try: import simplejson as json
except ImportError: import json


def Apps(request):
	usuarios = User.objects.all()
	return render_to_response('Apps.html', context_instance=RequestContext(request,{'usuarios':usuarios}))

def NuevoUsuario(request):
    if request.method=='POST':
        formulario = UserCreationForm(request.POST)
        if formulario.is_valid:
            formulario.save()
            return HttpResponseRedirect('/')
    else:
        formulario = UserCreationForm()
        
    return render_to_response('NuevoUsuario.html',{'formulario':formulario}, context_instance=RequestContext(request))


def AgregarUsuarioAjax(request):
    if request.is_ajax() and request.method == 'POST':
        formulario = UsuariosForm(request.POST)
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
def eliminar(request,id_usuario):
    usuario = Datos.objects.get(pk=id_usuario)
    usuario.delete()
    return HttpResponseRedirect("/")

def editar(request,id_usuario):
    usuario = Datos.objects.get(pk=id_usuario)
    #if request.method == "POST":
        #formulario = UsuariosForm(request.POST,instance=usuario)
        #if formulario.is_valid():
            #formulario.save()
            #return HttpResponseRedirect("/")
    #else:
    formulario=UsuariosForm(instance=usuario)
    return render_to_response('editarUsuario.html', context_instance=RequestContext(request,{'formulario':formulario}))

def editarUsuarioAjax(request):
    if request.is_ajax() and request.method == 'POST':
        usuario = Datos.objects.get(pk=request.POST['id_usuario'])
        formulario = UsuariosForm(request.POST, instance=usuario)
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