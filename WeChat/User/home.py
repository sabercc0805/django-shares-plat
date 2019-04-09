import os
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from User import models
from datetime import datetime
from .forms import UserForm
from .forms import UserInfoForm
from .forms import ChangePwdForm
from .forms import RegisterForm
from django.forms.models import model_to_dict
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@csrf_exempt
@csrf_protect


def iframe(request):
    kind = 0

    if not request.session.get('is_login', None):
        return redirect('/index/')

    model = request.session['model']
    if model != 1000:
        return redirect("/logout/")

    keypath=articletitle = request.GET.get('key')

    if not keypath:
        raise Http404("html does not exist")

    filepath=os.path.join("..\templates\centerdata", keypath)

    return render(request, filepath)

def showdata(request):
    kind = 0

    if not request.session.get('is_login', None):
        return redirect('/index/')

    model = request.session['model']
    if model != 1000:
        return redirect("/logout/")

    message = 1
    if request.method == "POST":
        iddate = request.POST["inputdate"]
        #后面根据用户级别显示相应日期数据********************************
        if iddate:
            try:
                message = 2
                centerdata = models.CenterData.objects.get(iddate=iddate)
                trend=centerdata.trend
                judge=centerdata.judge
                valueone=centerdata.valueone
                keypath=centerdata.filepath
                dateinit=iddate
                return render(request, 'showdatacommon.html', locals())
            except:
                message = 0

    #选择日期当天无数据，或者刚进入Get，获取最近一天数据显示
    centerdata = models.CenterData.objects.all().aggregate(Max('iddate'))
    trend = centerdata.trend
    judge = centerdata.judge
    valueone = centerdata.valueone
    keypath = centerdata.filepath
    dateinit=centerdata.iddate

    return render(request, 'showdatacommon.html', locals())


def homepage(request):
    return render(request, "form.html")


def index(request):
   kind = 0
   return render(request, 'index.html',locals())



def login(request):
    kind = 0
    if request.session.get('is_login',None):
        model = request.session['model']
        if model != 1000:
            return redirect('/logout/')

    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.Commonuser.objects.get(userid=username)
                if user.password == password:
                    request.session['is_login'] = True
                    request.session['user_id'] = user.userid
                    request.session['user_name'] = user.userid
                    request.session['password'] = user.password
                    request.session['level'] = user.level
                    dt = user.registerdate
                    request.session['registerdate'] = dt.strftime( '%Y-%m-%d %H:%M:%S')
                    request.session['currentdate'] = user.currentrecharge
                    request.session['model'] = 1000
                    return redirect('/index/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'login.html', locals())
    login_form = UserForm()
    return render(request, 'login.html', locals())


def logout(request):
    kind = 0
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/index/")
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/index/")

def register(request):
    kind = 0
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            phonenumber = register_form.cleaned_data['phonenumber']
            #if len(phonenumber) != 11:
            #message = "手机号码为11位！"
            #return render(request, 'register.html', locals())

            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'register.html', locals())
            else:
                same_name_user = models.Commonuser.objects.filter(userid=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'register.html', locals())
                same_phone_user = models.Commonuser.objects.filter(identify=phonenumber)
                if same_phone_user:  # 邮箱地址唯一
                    message = '该手机已被注册，请更换手机！'
                    return render(request, 'register.html', locals())

                # 当一切都OK的情况下，创建新用户
    #可能是django  bug  int类型字段直接等于会报错，必须在创建时赋值
                new_user = models.Commonuser.objects.create(userid = username,level=1)
               # new_user.userid = username
                new_user.password = password1
                new_user. identify = phonenumber
                new_user.acountuser = 'webregister'
                new_user.source =  'webregister'
                new_user.save()
                return redirect('/login/')  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'register.html', locals())


def userinfo(request):
    kind = 0

    if not request.session.get('is_login',None):
        return redirect('/index/')

    model =  request.session['model']
    if model != 1000:
        return redirect("/logout/")

    username = request.session['user_id']
    nlevel = request.session['level']
    registertime = request.session['registerdate']
    level = ""

    if nlevel == 1:
        level = "普通会员"
    else:
        level = "付费会员"

    UserInfo_form = UserInfoForm(locals())
    ChangePwd_form = ChangePwdForm()
    return render(request, 'userinfo.html',locals())

def article(request):
    kind = 0
    if not request.session.get('is_login',None):
        return redirect('/index/')

    model = request.session['model']
    if model != 1000:
        return redirect("/logout/")

    article_list = models.BlogArticle.objects.filter(delete_flag=0)


    paginator = Paginator(article_list, 10)
    # 从前端获取当前的页码数,默认为1
    page = request.GET.get('page', 1)

    #if int(page) > article_list.count()/10:
       # raise Http404("Page does not exist")
    # 把当前的页码数转换成整数类型
    currentPage = int(page)

    try:
        article_list = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        article_list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        article_list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容

    return render(request, 'article.html',locals())

def articlecontent(request):
    kind = 0
    if not request.session.get('is_login', None):
        return redirect('/index/')

    model = request.session['model']
    if model != 1000:
        return redirect("/logout/")

    titlename= request.GET.get('title')

    if titlename:
        acticle = models.BlogArticle.objects.get(title=titlename)
        userid = acticle.userid
        createtime = acticle.create_time
        clickrate = acticle.click_nums
        clickrate += 1
        models.BlogArticle.objects.filter(title=titlename).update(click_nums=clickrate)
        content =acticle.content
        return render(request, 'articlecontent.html', locals())
    else:
        raise Http404("文章不存在")


def changepassword(request):
    kind = 0

    if not request.session.get('is_login', None):
        return redirect('/index/')

    model = request.session['model']
    if model != 1000:
        return redirect("/logout/")

    username = request.session['user_id']
    nlevel = request.session['level']
    registertime = request.session['registerdate']
    level = ""

    if nlevel == 1:
        level = "普通会员"
    else:
        level = "付费会员"

    errortype = -1
    if request.method == "POST":
        ChangePwd_formPost = ChangePwdForm(request.POST)

        if ChangePwd_formPost.is_valid():
            password = ChangePwd_formPost.cleaned_data['oldpassword']
            newpassword1 = ChangePwd_formPost.cleaned_data['newpassword1']
            newpassword2 = ChangePwd_formPost.cleaned_data['newpassword2']

            if password == request.session['password']:
                if newpassword1 == newpassword2:
                    errortype = 0
                    request.session['password'] = newpassword1
                    models.Commonuser.objects.filter(userid=username).update(password=newpassword1)
                else:
                    errortype = 2
            else:
                errortype = 1

    UserInfo_form = UserInfoForm(locals())
    ChangePwd_form = ChangePwdForm()
    return render(request, 'userinfo.html', locals())