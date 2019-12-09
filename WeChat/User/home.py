import os
from django.utils import timezone
from django.http import FileResponse
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
from .forms import Commitform
from .forms import Creditform
from .forms import Coinform
from django.forms.models import model_to_dict
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.http import urlquote
from django.http import JsonResponse
from django.db.models import Q

from User.email import random_str  # 用于生成随机码
from User.email import send_code_email  # 用于生成随机码

from User.wechatpay import order_num
from User.wechatpay import opratecoinpool

@csrf_exempt
@csrf_protect

def iframe(request):
    kind = 0

    #if not request.session.get('is_login', None):
       # return redirect('/index/')

  #  model = request.session['model']
   # if model != 1000:
       # return redirect("/logout/")

    keypath = articletitle = request.GET.get('key')

    if not keypath:
        raise Http404("html does not exist")

    filepath = os.path.join("..\\templates\\centerdata", keypath)
    return render(request, filepath)

def showdata(request):
    kind = 0

    #if not request.session.get('is_login', None):
       # return redirect('/index/')

  #  model = request.session['model']
   # if model != 1000:
     #   return redirect("/logout/")

#目前所有等级用户均可查看所有天数数据
    message = 1

    datelist = []
    SSEList = []
    trendlist = []
    SSEListOne = []
    simSSElistOne = []
    SSEOne = 1
    simSSEOne = 1
    if request.method == "POST":
        iddate = request.POST["inputdate"]
        if iddate:
            try:
                message = 2
                centerdata = models.CenterData.objects.get(date=iddate)
                trend = centerdata.trend
                judge = centerdata.judge
                valueone = centerdata.valueone
                valuetwo = centerdata.valuetwo
                keypath = centerdata.filepath
                dateinit = iddate
                data_list = models.CenterData.objects.filter(date__lte=dateinit).order_by('-date')
                size = len(data_list)
                if size > 29:
                    SSEOne = data_list[29].valueone
                    simSSEOne = data_list[29].valuetwo
                    for i in range(0, 30):
                        datelist.append(data_list[i].date)

                        color = ""
                        if data_list[i].trend < 2:
                            color = "#FF0000"
                        else:
                            color = "#00FF00"

                        ssedict = {'y': data_list[i].valueone, 'color': color}
                        SSEList.append(ssedict)

                        trendlist.append(data_list[i].trend)
                        SSEListOne.append(round(data_list[i].valueone / SSEOne, 2))
                        simSSElistOne.append(round(data_list[i].valuetwo / simSSEOne, 2))
                else:
                    SSEOne = data_list[size - 1].valueone
                    simSSEOne = data_list[size - 1].valuetwo
                    for i in range(size):
                        datelist.append(data_list[i].date)
                        color = ""
                        if data_list[i].trend < 2:
                            color = "#FF0000"
                        else:
                            color = "#00FF00"

                        ssedict = {'y': data_list[i].valueone, 'color': color}
                        SSEList.append(ssedict)
                        trendlist.append(data_list[i].trend)
                        SSEListOne.append(round(data_list[i].valueone / SSEOne, 2))
                        simSSElistOne.append(round(data_list[i].valuetwo / simSSEOne, 2))

                datelist.reverse();
                SSEList.reverse();
                trendlist.reverse();
                SSEListOne.reverse();
                simSSElistOne.reverse();

                if len(judge) > 0:
                    text = judge
                    return render(request, 'showdatacommon.html', locals())

                return render(request, 'showdatacommon.html', locals())
            except:
                message = 0

    # 选择日期当天无数据，或者刚进入Get，获取最近一天数据显示

    try:
        centerdata = models.CenterData.objects.all().order_by("-date")[0]

        trend = centerdata.trend
        judge = centerdata.judge
        valueone = centerdata.valueone
        valuetwo = centerdata.valuetwo
        keypath = centerdata.filepath
        dateinit = centerdata.date
        data_list = models.CenterData.objects.filter(date__lte=dateinit).order_by('-date')
        size = len(data_list)
        if size > 29:
            SSEOne = data_list[29].valueone
            simSSEOne = data_list[29].valuetwo
            for i in range(0, 30):
                datelist.append(data_list[i].date)

                color = ""
                if data_list[i].trend < 2:
                    color = "#FF0000"
                else:
                    color = "#00FF00"

                ssedict = {'y': data_list[i].valueone, 'color': color}
                SSEList.append(ssedict)

                trendlist.append(data_list[i].trend)
                SSEListOne.append(round(data_list[i].valueone / SSEOne, 2))
                simSSElistOne.append(round(data_list[i].valuetwo / simSSEOne, 2))
        else:
            SSEOne = data_list[size - 1].valueone
            simSSEOne = data_list[size - 1].valuetwo
            for i in range(size):
                datelist.append(data_list[i].date)

                color = ""
                if data_list[i].trend < 2:
                    color = "#FF0000"
                else:
                    color = "#00FF00"

                ssedict = {"y": data_list[i].valueone, "color": color}
                SSEList.append(ssedict)

                trendlist.append(data_list[i].trend)
                SSEListOne.append(round(data_list[i].valueone / SSEOne, 2))
                simSSElistOne.append(round(data_list[i].valuetwo / simSSEOne, 2))

        datelist.reverse();
        SSEList.reverse();
        trendlist.reverse();
        SSEListOne.reverse();
        simSSElistOne.reverse();

        message = 2

        if len(judge) > 0:
            text = judge
            return render(request, 'showdatacommon.html', locals())

        return render(request, 'showdatacommon.html', locals())
    except:
        return render(request, 'index.html', locals())


def homepage(request):
    return render(request, "form.html")

def advertisement(request):
    kind = 0
    return render(request, "ad.html", locals())


def index(request):
   kind = 0

   if not request.session.get('is_login', None):
       return render(request, 'index.html', locals())

   model = request.session['model']
   if model != 1000:
       return redirect("/logout/")

   return render(request, 'index.html', locals())

def about(request):
   kind = 0
   return render(request, 'about.html', locals())


def login(request):
    kind = 0
    if request.session.get('is_login',None):
        model = request.session['model']
        if model != 1000:
            return redirect('/logout/')
        else:
            return redirect('/index/')

    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.Commonuser.objects.get(userid=username)
                if user.password == password:
                    #nowTime = datetime.datetime.now().strftime('YYYY-MM-DD HH:MM:SS')
                    #user.currnetlogindate = datetime.datetime.now()
                    user.save()
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
            codeinput = register_form.cleaned_data['code']
            #if len(phonenumber) != 11:
            #message = "手机号码为11位！"
            #return render(request, 'register.html', locals())
            agreement = request.POST.getlist('protocol')
            if len(agreement) == 0:
                message = "请先同意用户协议，再进行注册！"
                register_form = RegisterForm(locals())
                return render(request, 'register.html', locals())

            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                register_form = RegisterForm(locals())
                return render(request, 'register.html', locals())
            else:
                try:
                    same_name_user = models.Commonuser.objects.get(userid=username)# 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    register_form = RegisterForm(locals())
                    return render(request, 'register.html', locals())
                except:
                    state = 1

                try:
                    same_phone_user = models.Commonuser.objects.get(identify=phonenumber)# 邮箱地址唯一
                    message = '该邮箱已被注册，请更换邮箱！'
                    register_form = RegisterForm(locals())
                    return render(request, 'register.html', locals())
                except:
                    state = 1

                try:
                    codeobj = models.Code.objects.get(email=phonenumber)

                    if codeobj.codeid != codeinput:
                        message = '激活码错误，请重新获取激活码！'
                        register_form = RegisterForm(locals())
                        return render(request, 'register.html', locals())

                    getdate = codeobj.gettime
                    strdate = getdate.strftime("%Y-%m-%d %H:%M:%S")
                    beforedate = datetime.strptime(strdate, '%Y-%m-%d %H:%M:%S')
                    nowdate = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
                    trandate = datetime.strptime(nowdate, '%Y-%m-%d %H:%M:%S')

                    delta = trandate - beforedate
                    interval = delta.seconds
                    if interval/60 > 5:
                        message = '激活码超时，请重新获取激活码！'
                        register_form = RegisterForm(locals())
                        return render(request, 'register.html', locals())

                    codeobj.delete()
                except:
                    message = '激活失败，请重新获取激活码！'
                    register_form = RegisterForm(locals())
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
                return render(request, 'registertran.html') # 自动跳转到登录页面
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

    try:
        User = models.Commonuser.objects.get(userid=username)
        ChangePwd_form = ChangePwdForm()
        type = 0
        signed = 0
        fengyacoin = int(User.fengyacoin/100)
        try:
            signdate = User.signdate
            beforedate = datetime.strptime(signdate, '%Y-%m-%d')
            nowdate =timezone.now().strftime("%Y-%m-%d")
            trandate = datetime.strptime(nowdate, '%Y-%m-%d')

            delta = trandate - beforedate
            interval = delta.days
            if interval == 0:
                signed = 1
        except:
            signed = 0

        return render(request, 'userinfoshow.html', locals())
    except:
        render(request, 'commontran.html')


'''
    username = request.session['user_id']
    nlevel = request.session['level']
    registertime = request.session['registerdate']
    level = ""

    if nlevel == 1:
        level = "普通会员"
    elif nlevel == 2:
        level = "超级会员"
    elif nlevel == 3:
        level = "白金会员"
    elif nlevel == 4:
        level = "钻石会员"
'''

def article(request):
    kind = 0
    #article_list = [];
    #if not request.session.get('is_login',None):
      #  article_list = models.BlogArticle.objects.filter(delete_flag=0,user_right=0)
   # else:
        #model = request.session['model']
        #if model != 1000:
            #return redirect("/logout/")
    top_list = []
    common_list = []
    article_list = []
    search = ''
    if request.method == "POST":
        search = request.POST["searchinfo"]
    else:
        search = request.GET.get("searchinfo", '')

    tag = request.GET.get('tag',None)

    if len(search) == 0:
        if not tag:
            top_list = models.BlogArticle.objects.filter(delete_flag=0, top=1).order_by('-create_time')
            common_list = models.BlogArticle.objects.filter(delete_flag=0, top=0).order_by('-create_time')
            tag = '全部'
        else:
            if tag == '全部':
                top_list = models.BlogArticle.objects.filter(delete_flag=0, top=1).order_by('-create_time')
                common_list = models.BlogArticle.objects.filter(delete_flag=0, top=0).order_by('-create_time')
            else:
                tag = request.GET.get('tag')
                top_list = models.BlogArticle.objects.filter(delete_flag=0, top=1, tag=tag ).order_by('-create_time')
                common_list = models.BlogArticle.objects.filter(delete_flag=0, top=0, tag=tag).order_by('-create_time')
    else:
        if not tag:
            top_list = models.BlogArticle.objects.filter(delete_flag=0, title__icontains=search, top=1).order_by('-create_time')
            common_list = models.BlogArticle.objects.filter(delete_flag=0, title__icontains=search, top=0).order_by('-create_time')
            tag = '全部'
        else:
            if tag == '全部':
                top_list = models.BlogArticle.objects.filter(delete_flag=0, title__icontains=search, top=1).order_by('-create_time')
                common_list = models.BlogArticle.objects.filter(delete_flag=0, title__icontains=search, top=0).order_by('-create_time')
            else:
                tag = request.GET.get('tag')
                top_list = models.BlogArticle.objects.filter(delete_flag=0, tag=tag, title__icontains=search, top=1).order_by( '-create_time')
                common_list = models.BlogArticle.objects.filter(delete_flag=0, tag=tag, title__icontains=search, top=0).order_by('-create_time')

    for object in top_list:
        article_list.append(object)

    for object in common_list:
        article_list.append(object)

    currentPage = request.GET.get('currentPage')
    tag_list = models.BlogTag.objects.filter()

    paginator = Paginator(article_list, 15)
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

    return render(request, 'articlenew.html',locals())

def articlecontent(request):
    kind = 0
    coin = 0
    integral = 0
    days = 0
    commitnum = 0
    collectcount = 0
    commitflag = 0
    cancommit = 0
    finger = 0
    bcollect = 0
    filecosttype = 0
    username = ""
    titlename = request.GET.get('title')
    currentPage = request.GET.get('currentPage')

    if not currentPage:
        currentPage = 1

    if not request.session.get('is_login', None):
        acticletran = models.BlogArticle.objects.get(title=titlename)

        if not acticletran:
            situation = 1
            return render(request, 'articletran.html', {"currentPage": currentPage, 'situation': situation})
        else:
            if acticletran.user_right != 0:
                return render(request, 'articletran.html', {"currentPage": currentPage})
    else:
        model = request.session['model']
        if model != 1000:
            return redirect("/logout/")

        situation = 0
        username = request.session['user_id']
        #判断是否需要积分或者缝芽币# 0免费
        if titlename:
            try:
                acticlejudge = models.BlogArticle.objects.get(title=titlename)
                userinfo = models.Commonuser.objects.get(userid=username)
                coin = int(userinfo.fengyacoin/100)
                integral = userinfo.integrate
                filecosttype = acticlejudge.filecosttype
                #查找一下在已有列表中是否存在如果存在不再重复扣费
                try:
                    arcticlecontain = models.ArticleContain.objects.get(title=titlename,userid=username)
                    finger = arcticlecontain.finger
                    bcollect = arcticlecontain.collect
                    commitflag = arcticlecontain.commentflag
                except:
                    if acticlejudge.articlecosttype == 1:
                        integrate = acticlejudge.articlecost
                        if userinfo.integrate < integrate:
                            situation = 2
                            return render(request, 'articletran.html',
                                          {"currentPage": currentPage, 'situation': situation})
                        else:
                            integrate = userinfo.integrate - integrate
                            models.Commonuser.objects.filter(userid=username).update(integrate=integrate)
                            integral = integrate

                    elif acticlejudge.articlecosttype == 2:
                        fengyacoin = acticlejudge.articlecost*100
                        if userinfo.fengyacoin < fengyacoin:
                            situation = 3
                            return render(request, 'articletran.html',
                                          {"currentPage": currentPage, 'situation': situation})
                        else:
                            opratecoinpool(fengyacoin)
                            fengyacoin = userinfo.fengyacoin - fengyacoin
                            models.Commonuser.objects.filter(userid=username).update(fengyacoin=fengyacoin)
                            coin = fengyacoin/100
                    new_data = models.ArticleContain.objects.create(title=titlename,userid=username,costtype=acticlejudge.articlecosttype,cost=acticlejudge.articlecost,tag=acticlejudge.tag)
                    new_data.save()
            except:
                situation = 1
                return render(request, 'articletran.html', {"currentPage": currentPage,'situation':situation})

         #获取用户收藏列表#
        collectlist = models.ArticleContain.objects.filter(userid=username, collect=1).order_by('-firstreaddate')[:10]

        if not collectlist:
            collectcount = 0
        else:
            collectcount = collectlist.count()
        #获取用户评论文章数
        commitUserList = models.ArticleContain.objects.filter(userid=username,commentflag=2)

        if commitUserList:
            commitnum = commitUserList.count()


    if titlename:
        acticle = models.BlogArticle.objects.get(title=titlename)
        userid = acticle.userid
        createtime = acticle.create_time
        clickrate = acticle.click_nums
        right = acticle.user_right
        clickrate += 1
        models.BlogArticle.objects.filter(title=titlename).update(click_nums=clickrate)
        content =acticle.content
        filepath = acticle.filepath
        tag = acticle.tag
        cancommit = acticle.cancommit
        commit_form = Commitform()
        if acticle.user_right != 0:
            nLevel = request.session['level']
            if nLevel < right:
                return render(request, 'articletran.html', {"currentPage": currentPage})

            # 获取该文章评论列表
        if cancommit == 2:
            commitlist = models.SpecialCommit.objects.filter(title=titlename, commentflag=2).order_by('-firstreaddate')#y用户自己评论，最新的在上面
        else:
            commitlist = models.ArticleContain.objects.filter(title=titlename, commentflag=2).order_by('firstreaddate')

        recommendlist = models.BlogArticle.objects.filter(tag=tag,delete_flag=0).order_by('-create_time')[:10]

        if recommendlist.count() < 10:
            size = 10 - recommendlist.count()
            addlist = models.BlogArticle.objects.filter(~Q(tag=tag),delete_flag=0).order_by('-create_time')[:size]
            try:
                if addlist:
                    recommendlist.extend(addlist)
            except:
                recommendlist = addlist

        if (len(filepath) > 0):
            cost = acticle.cost
            filename = filepath
            return render(request, 'articlecontentnew.html', locals())
        else:
            return render(request, 'articlecontentnew.html', locals())
    else:
        situation = 1
        return render(request, 'articletran.html', {"currentPage": currentPage, 'situation': situation})


def download(request):
    kind = 0
    titlename = request.GET.get('title')
    filename = request.GET.get('filename')
    acticle = models.BlogArticle.objects.get(title=titlename)
    if not request.session.get('is_login', None):
        if acticle.user_right == 0:
            savepath = "C:\\articlefile\\" + titlename
            file = open(os.path.join(savepath, filename), 'rb')
            response = FileResponse(file)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="%s"' % (urlquote(filename))
            return response
        else:
            return redirect('/index/')

    model = request.session['model']
    if model != 1000:
        return redirect("/logout/")

    # 还要建一张表如果用户已下载该资源则下次再下载无需花费积分
    titlename = request.GET.get('title')
    filename = request.GET.get('filename')
    currentPage = request.GET.get('currentPage')
    userid = request.session['user_id']


    fileobj = models.Fileright.objects.filter(userid=userid, title=titlename)
    if fileobj.count() == 0:
        if acticle.user_right == 0:
            savepath = "C:\\articlefile\\" + titlename
            file = open(os.path.join(savepath, filename), 'rb')
            response = FileResponse(file)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="%s"' % (urlquote(filename))
            return response
        else:
            userinfo = models.Commonuser.objects.get(userid=userid)
            fengyacoin = userinfo.fengyacoin
            intergrate = userinfo.integrate
            articleblog = models.BlogArticle.objects.get(title=titlename)
            filecosttype = articleblog.filecosttype
            cost = articleblog.cost
            userbalance = 0
            if filecosttype == 1:
                userbalance = intergrate - int(cost)
            elif filecosttype == 2:
                userbalance = fengyacoin - int(cost)*100

            if userbalance >= 0:
                try:
                    if filecosttype == 1:
                        userinfo.integrate = userbalance
                        userinfo.save()
                    elif filecosttype == 2:
                        opratecoinpool(int(cost)*100)
                        userinfo.fengyacoin = userbalance
                        userinfo.save()

                    models.Fileright.objects.create(userid=userid, title=titlename,costtype=filecosttype,cost=articleblog.cost,tag=articleblog.tag)
                    savepath = "C:\\articlefile\\" + titlename
                    file = open(os.path.join(savepath, filename), 'rb')
                    response = FileResponse(file)
                    response['Content-Type'] = 'application/octet-stream'
                    response['Content-Disposition'] = 'attachment;filename="%s"' % (urlquote(filename))
                    return response
                except:
                    return render(request, 'downtran.html',
                                  {"errortype": 1, "titlename": titlename, "currentPage": currentPage})
            else:
                last = 0
                errortype = 1
                if filecosttype == 1:
                    errortype = 2
                    last = userinfo.integrate
                elif filecosttype == 2:
                    errortype = 3
                    last = userinfo.fengyacoin/100

                return render(request, 'downtran.html',
                              {"errortype": errortype, "titlename": titlename, "currentPage": currentPage, "last": last})
    else:
        savepath = "C:\\articlefile\\" + titlename
        file = open(os.path.join(savepath, filename), 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="%s"' % (urlquote(filename))
        return response





def changepassword(request):
    kind = 0

    if not request.session.get('is_login', None):
        return redirect('/index/')

    model = request.session['model']
    if model != 1000:
        return redirect("/logout/")

    username = request.session['user_id']

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
    try:
        User = models.Commonuser.objects.get(userid=username)
        ChangePwd_form = ChangePwdForm()
        type = 0
        return render(request, 'userinfoshow.html', locals())
    except:
        return render(request,"commontran.html")

################ajax返回#############################
#####用户点赞#########

def ajax_finger(request):
    figer = 0
    if not request.session.get('is_login', None):
        figer = -2
        return JsonResponse(figer, safe=False)

    title=request.GET.get('title')
    username = request.session['user_id']


    try:
        article = models.ArticleContain.objects.filter(userid=username,title=title)
        articleblog = models.BlogArticle.objects.get(title=title)
        scorenum = articleblog.scorernumber
        if article[0].finger == 1:
            figer = 0
            scorenum -= 1
            models.ArticleContain.objects.filter(userid=username, title=title).update(finger=0)
            models.BlogArticle.objects.filter(title=title).update(scorernumber=scorenum)
        elif article[0].finger == 0:
            figer = 1
            scorenum += 1
            models.ArticleContain.objects.filter(userid=username, title=title).update(finger=1)
            models.BlogArticle.objects.filter(title=title).update(scorernumber=scorenum)

        return JsonResponse(figer, safe=False)
    except:
        figer = -1
        return JsonResponse(figer, safe=False)


#####用户收藏#########
def ajax_collect(request):
    bcollect = 0
    if not request.session.get('is_login', None):
        bcollect = -2
        return JsonResponse(bcollect, safe=False)

    title=request.GET.get('title')
    username = request.session['user_id']


    try:
        article = models.ArticleContain.objects.filter(userid=username,title=title)
        if article[0].collect == 1:
            bcollect = 0
            models.ArticleContain.objects.filter(userid=username, title=title).update(collect=0)
        elif article[0].collect == 0:
            bcollect = 1
            models.ArticleContain.objects.filter(userid=username, title=title).update(collect=1)

        return JsonResponse(bcollect, safe=False)
    except:
        bcollect = -1
        return JsonResponse(bcollect, safe=False)

##########提交评论###########################
def ajax_commit(request):
    bcommit = 0
    if not request.session.get('is_login', None):
        return redirect('/index/')

    model = request.session['model']
    if model != 1000:
        return redirect("/logout/")

    if request.method == "POST":
        title = request.POST.get('title')
        commentflag = int(request.POST.get('commentflag'))
        username = request.session['user_id']
        commitcontent = request.POST.get("commitcontent")

        try:
            bcommit = 1
            if commentflag == 2:
                bcommit = 2
                commit = models.SpecialCommit.objects.create(userid=username, title=title, comment=commitcontent)
                commit.save()
            else:
                bcommit = 1
                article = models.ArticleContain.objects.get(userid=username, title=title)
                article.comment = commitcontent
                article.commentflag = 1
                article.save()


            return JsonResponse(bcommit, safe=False)
        except:
            bcommit = -1
            return JsonResponse(bcommit, safe=False)
    else:
        return redirect("/logout/")

def userarticleoperate(request):
    kind = 0

    if not request.session.get('is_login', None):
        return redirect('/index/')

    model = request.session['model']
    if model != 1000:
        return redirect("/logout/")

    type = request.GET.get('type',0) #1：教程历史；2、收藏；3、点赞；4、下载
    type = int(type)
    username = request.session['user_id']
    article_list = []
    oprateinfo = ""
    try:
        if type == 1:
            contentname = "历史教程"
            oprateinfo = "历史教程"
            article_list = models.ArticleContain.objects.filter(userid=username).order_by('-firstreaddate')
        elif type == 2:
            contentname = "我的收藏"
            oprateinfo = "收藏"
            article_list = models.ArticleContain.objects.filter(userid=username, collect=1).order_by('-firstreaddate')
        elif type == 3:
            contentname = "我的点赞"
            oprateinfo = "点赞"
            article_list = models.ArticleContain.objects.filter(userid=username, finger=1).order_by('-firstreaddate')
        elif type == 4:
            contentname = "我的下载"
            oprateinfo = "下载"
            article_list = models.Fileright.objects.filter(userid=username).order_by('-buydate')
        else:
            return render(request, 'commontran.html')
    except:
        return render(request, 'commontran.html')

    if article_list.count() == 0:
        return render(request, 'userarticlenone.html',locals())

    paginator = Paginator(article_list, 10)
    # 从前端获取当前的页码数,默认为1
    page = request.GET.get('page', 1)

    # if int(page) > article_list.count()/10:
    # raise Http404("Page does not exist")
    # 把当前的页码数转换成整数类型
    currentPage = 1
    try:
        currentPage = int(page)
    except:
        currentPage = 1

    try:
        article_list = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        article_list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        article_list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容

    return render(request, 'userarticleinfo.html', locals())

def usercancel(request):
    kind = 0

    if not request.session.get('is_login', None):
        return redirect('/index/')

    model = request.session['model']
    if model != 1000:
        return redirect("/logout/")

    type = request.GET.get('type',0)  # 1：教程历史；2、收藏；3、点赞；4、下载
    type = int(type)
    titlename = request.GET.get('titlename')
    username = request.session['user_id']
    article_list = []
    oprateinfo = ""

    try:
        userarticle = models.ArticleContain.objects.get(userid=username,title=titlename)
        if type == 2:
            userarticle.collect = 0
            userarticle.save()
            contentname = "我的收藏"
            oprateinfo = "收藏"
            article_list = models.ArticleContain.objects.filter(userid=username, collect=1).order_by('-firstreaddate')
        elif type == 3:
            userarticle.finger = 0
            userarticle.save()
            contentname = "我的点赞"
            oprateinfo = "点赞"
            article_list = models.ArticleContain.objects.filter(userid=username, finger=1).order_by('-firstreaddate')
    except:
        return render(request, 'commontran.html')

    if article_list.count() == 0:
        return render(request, 'userarticlenone.html',locals())

    paginator = Paginator(article_list, 10)
    # 从前端获取当前的页码数,默认为1
    page = request.GET.get('page', 1)

    # if int(page) > article_list.count()/10:
    # raise Http404("Page does not exist")
    # 把当前的页码数转换成整数类型
    currentPage = int(page)

    try:
        article_list = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        article_list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        article_list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    return render(request, 'userarticleinfo.html', locals())

def ajax_sign(request):
    bcommit = 0
    if not request.session.get('is_login', None):
        return redirect('/index/')

    model = request.session['model']
    if model != 1000:
        return redirect("/logout/")


    username = request.session['user_id']

#签到获取积分在充值处一起做
    bsign = 1

    try:
        keeplogin = 0
        user = models.Commonuser.objects.get(userid=username)
        credit = user.integrate

        switch = {
            1: 10,
            2: 15,
            3: 20,
            4: 25,
            5: 30,
            6: 35,
            7: 40,
        }
        try:
            signdate = user.signdate
            beforedate = datetime.strptime(signdate, '%Y-%m-%d')
            nowdate = timezone.now().strftime("%Y-%m-%d")
            trandate = datetime.strptime(nowdate, '%Y-%m-%d')

            delta = trandate - beforedate
            interval = delta.days
            keeplogin = user.keeplogin

            if interval == 0:
                return JsonResponse(0, safe=False)
            elif interval != 1:
                keeplogin = 1
            else:
                keeplogin += 1

            if keeplogin < 7:
                credit += switch[keeplogin]
            else:
                credit += switch[7]

            nowTime = timezone.now().strftime('%Y-%m-%d')
            models.Commonuser.objects.filter(userid=username).update(signdate=nowTime, keeplogin=keeplogin,integrate=credit)
        except:
            keeplogin = 1
            credit += switch[keeplogin]
            nowTime = timezone.now().strftime("%Y-%m-%d")
            models.Commonuser.objects.filter(userid=username).update(signdate=nowTime,keeplogin=1,integrate=credit)

        return JsonResponse(keeplogin, safe=False)
    except:
        bsign = -1
        return JsonResponse(bsign, safe=False)

def credits(request):
    kind = 0

    if not request.session.get('is_login', None):
        return redirect('/index/')

    model = request.session['model']
    if model != 1000:
        return redirect("/logout/")

    type = request.GET.get('type', 0)
    type = int(type)
    credit_form = Creditform()
    return render(request, 'intergrate.html', locals())

def coin(request):
    kind = 0

    if not request.session.get('is_login', None):
        return redirect('/index/')

    model = request.session['model']
    if model != 1000:
        return redirect("/logout/")

    type = request.GET.get('type', 0)  # 1：教程历史；2、收藏；3、点赞；4、下载
    type = int(type)
    coin_form = Coinform()

    return render(request, 'coin.html', locals())

def exchange(request):
    kind = 0

    if not request.session.get('is_login', None):
        return redirect('/index/')

    model = request.session['model']
    if model != 1000:
        return redirect("/logout/")

    if request.method == "POST":
        credit_form = Creditform(request.POST)
        exchangetype = 0
        success = 0
        if credit_form.is_valid():
            exchangetype = int(credit_form.cleaned_data['exchangetype'])
        else:
            chargetype = -2
            return render(request, 'chargetran.html', {"chargetype": chargetype, "success": success})

        username = request.session['user_id']
        precent = 100
        credit = 0

        switch = {
            0: 10,
            1: 50,
            2: 100,
            3: 500,
            4: 1000,
            5: 2000,
            6: 3000,
            7: 5000,
        }

        try:
            credit = switch[exchangetype]
        except:
            credit = 0

        ordertype = ""
        if exchangetype > 9:
            ordertype = "2" + str(exchangetype)
        else:
            ordertype = "20" + str(exchangetype)

        if credit <= 0 | len(ordertype) == 0:
            chargetype = -2
            return render(request, 'chargetran.html', {"chargetype":chargetype,"success":success})

        coin = credit/10*100
        coin = coin*precent/100
        try:
            User = models.Commonuser.objects.get(userid=username)
            usercoin = User.fengyacoin
            usergrate = User.integrate
            if usercoin > coin:
                #获取订单号
                orderid = order_num(ordertype,username)
                #创建订单
                new_credit = models.CreditExchange.objects.create(orderid=orderid,coin=coin,integrate=credit,userid=username,precent=precent)
                new_credit.save();
                try:
                    usercoin -= coin
                    usergrate += credit
                    models.Commonuser.objects.filter(userid=username).update(fengyacoin=usercoin,integrate=usergrate)
                    #F函数更新coinpool 并发小心
                    try:
                        opratecoinpool(coin)
                        new_credit.orderstate = 1
                        new_credit.save()
                    except:
                        new_credit.orderstate = -1
                        new_credit.save()

                    content = "兑换"
                    num = credit
                    unit= "积分"
                    success = 1
                    return render(request, 'chargetran.html',locals())
                except:
                    chargetype = -2
                    return render(request, 'chargetran.html', {"chargetype": chargetype, "success": success})
            else:
                chargetype = -1
                return render(request, 'chargetran.html', {"chargetype": chargetype, "success": success})
        except:
            chargetype = -2
            return render(request, 'chargetran.html', {"chargetype": chargetype,"success":success})

        return redirect('/userinfo/')
    else:
        return redirect('/index/')

def checkorder(request):
    kind = 0

    if not request.session.get('is_login', None):
        return redirect('/index/')

    model = request.session['model']
    if model != 1000:
        return redirect("/logout/")

    username = request.session['user_id']
    orderid = request.GET.get('orderid',"")

    result = -1
    try:
        orderover = models.OrderOver.objects.get(userid=username,orderid=orderid)
        if orderover.orderstate == 1:
            result = 1
        elif orderover.orderstate == 0:
            result = 0
    except:
        result = -1

    return JsonResponse(result, safe=False)

def chargeresult(request):
    kind = 0

    if not request.session.get('is_login', None):
        return redirect('/index/')

    model = request.session['model']
    if model != 1000:
        return redirect("/logout/")

    username = request.session['user_id']
    success = int(request.GET.get('result', 0))
    orderid = request.GET.get('orderid', "")
    num = 0
    if success == 1:
        orderover = models.OrderOver.objects.get(userid=username, orderid=orderid)
        num = orderover.coin

    content = "充值"
    unit = "缝芽币"
    chargetype = 1
    return render(request, 'chargetran.html', locals())

def ceshi(request):
    return render(request, 'pay.html')

def orderlist(request):
    kind = 0

    if not request.session.get('is_login', None):
        return redirect('/index/')

    model = request.session['model']
    if model != 1000:
        return redirect("/logout/")

    order_list = []
    over_list = []
    start_list = []
    username = request.session['user_id']
    ordertype = int(request.GET.get('ordertype', 1))
    type = int(request.GET.get('type',0))
    try:
        if ordertype == 1:
            over_list = models.OrderOver.objects.filter(userid=username).order_by('-chargedate')
            start_list = models.OrderStart.objects.filter(userid=username).order_by('-chargedate')
            if over_list.count() > 0 & start_list.count() > 0:
                over_list.extend(start_list)
                order_list = over_list
            elif over_list.count() > 0:
                order_list = over_list
            elif start_list.count() > 0:
                order_list = start_list
        elif ordertype == 2:
            order_list = models.CreditExchange.objects.filter(userid=username).order_by('-exchangedate')
    except:
        render(request, 'commontran.html')

    if len(order_list) == 0:
        oprateinfo = ''
        if ordertype == 1:
            oprateinfo = '缝芽币充值'
        elif ordertype == 2:
            oprateinfo = '积分兑换'
        return render(request, 'orderone.html', locals())

    paginator = Paginator(order_list, 15)
    # 从前端获取当前的页码数,默认为1
    page = request.GET.get('page', 1)

    #if int(page) > article_list.count()/10:
       # raise Http404("Page does not exist")
    # 把当前的页码数转换成整数类型
    currentPage = int(page)

    try:
        order_list = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        order_list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        order_list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容

    return render(request, 'orderlist.html',locals())

def ajax_apeal(request):#申诉用post
    kind = 0

    if not request.session.get('is_login', None):
        return redirect('/index/')

    model = request.session['model']
    if model != 1000:
        return redirect("/logout/")

    username = request.session['user_id']

    if request.method == "POST":
        ordertype = request.POST["ordertype"]
        orderstate = request.POST["orderstate"]
        orderid = request.POST["orderid"]
        if int(ordertype) == 1:
            try:
                if int(orderstate) < 0:
                    models.OrderStart.objects.filter(userid=username, orderid=orderid).update(appeal=1)
                else:
                    models.OrderOver.objects.filter(userid=username,orderid=orderid).update(appeal=1)

                return JsonResponse(1, safe=False)
            except:
                return JsonResponse(-1, safe=False)
        elif int(ordertype) == 2:
            try:
                models.CreditExchange.objects.filter(userid=username,orderid=orderid).update(appeal=1)
                return JsonResponse(1, safe=False)
            except:
                return JsonResponse(-1, safe=False)

    else:
        return JsonResponse(-1, safe=False)

def ajax_getcode(request):#获取激活码

    if request.method == "POST":
        email = request.POST["email"]
        if len(email) == 0:
            return JsonResponse(0, safe=False)

        str = ""
        try:
            User = models.Commonuser.objects.get(identify=email)
            username = User.userid
            return JsonResponse(-1, safe=False)
        except:
            str = random_str()

        try:
            code = models.Code.objects.get(email=email)
            code.codeid = str
            code.save()
        except:
            try:
                code = models.Code.objects.create(email=email, codeid=str)
                code.save()
            except:
                return JsonResponse(0, safe=False)

        if send_code_email(email, str):
            return JsonResponse(1, safe=False)
        else:
            return JsonResponse(0, safe=False)
    else:
        return JsonResponse(0, safe=False)


