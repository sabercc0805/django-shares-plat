import os
from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect



newpath=''

@csrf_exempt
@csrf_protect

def get_path(request):
    request.encoding = 'utf-8'
    #global  newpath
    #if 'pathname' in request.GET:
     #   newpath = request.GET['pathname']
    #    message = '你添加的路径为: ' +  newpath
   # else:
    #    message = '你提交了空表单'
   #     return render(request, 'no file path')
   # print(newpath)
    return render(request,"form.html")