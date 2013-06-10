# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from streaming.forms import *
from django.template.context import RequestContext
from streaming.models import *
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm,  AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate, logout 
from django.contrib.auth.decorators import login_required


def live(request):
	return render_to_response('streaming.html', context_instance=RequestContext(request))