import os
from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect


@csrf_exempt
@csrf_protect

def homepage(request):
    return render(request, "form.html")
