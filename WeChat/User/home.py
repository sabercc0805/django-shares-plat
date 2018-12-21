import os
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect


@csrf_exempt
@csrf_protect

def homepage(request):
    return render(request, "form.html")


def index(request):
    pass
    return render(request, 'base.html')


def login(request):
    pass
    return render(request, 'login.html')


def register(request):
    pass
    return render(request, 'register.html')


def logout(request):
    pass
    return redirect('/index/')