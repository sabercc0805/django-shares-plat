import os
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from User import models
from .forms import UserForm

@csrf_exempt
@csrf_protect

def homepage(request):
    return render(request, "form.html")


def index(request):
    pass
    return render(request, 'base.html')


def login(request):
    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.Commonuser.objects.get(userid=username)
                if user.password == password:
                    return redirect('/index/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'login.html', locals())
    login_form = UserForm()
    return render(request, 'login.html', locals())




def register(request):
    pass
    return render(request, 'register.html')


def logout(request):
    pass
    return redirect('/index/')