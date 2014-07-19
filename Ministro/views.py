from django.conf import settings
from django.shortcuts import render
from Ministro.models import *
from django.template.context import RequestContext
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

# Create your views here.

