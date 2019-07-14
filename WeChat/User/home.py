import os
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
from django.forms.models import model_to_dict
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.http import urlquote
from django.http import JsonResponse
from django.db.models import Q

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
                same_name_user = models.Commonuser.objects.get(userid=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    register_form = RegisterForm(locals())
                    return render(request, 'register.html', locals())
                same_phone_user = models.Commonuser.objects.get(identify=phonenumber)
                if same_phone_user:  # 邮箱地址唯一
                    message = '该邮箱已被注册，请更换邮箱！'
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
    elif nlevel == 2:
        level = "超级会员"
    elif nlevel == 3:
        level = "白金会员"
    elif nlevel == 4:
        level = "钻石会员"


    if request.method == "POST":
        UserInfo_form = UserInfoForm(request.POST)
        if UserInfo_form.is_valid():
            User = models.Commonuser.objects.get(userid=username)
            phonenum = User.phonenum
            email = User.identify
            coin = User.fengyacoin
            ChangePwd_form = ChangePwdForm()
            return render(request, 'userinfo.html', locals())

    User = models.Commonuser.objects.get(userid=username)
    phonenum = User.phonenum
    email = User.identify
    coin = User.fengyacoin
    UserInfo_form = UserInfoForm(locals())
    ChangePwd_form = ChangePwdForm()
    return render(request, 'userinfo.html',locals())

def article(request):
    kind = 0
    #article_list = [];
    #if not request.session.get('is_login',None):
      #  article_list = models.BlogArticle.objects.filter(delete_flag=0,user_right=0)
   # else:
        #model = request.session['model']
        #if model != 1000:
            #return redirect("/logout/")
    article_list = []
    search = ''
    if request.method == "POST":
        search = request.POST["searchinfo"]
    else:
        search = request.GET.get("searchinfo", '')

    tag = request.GET.get('tag',None)

    if len(search) == 0:
        if not tag:
            article_list = models.BlogArticle.objects.filter(delete_flag=0)
            tag = '全部'
        else:
            if tag == '全部':
                article_list = models.BlogArticle.objects.filter(delete_flag=0)
            else:
                tag = request.GET.get('tag')
                article_list = models.BlogArticle.objects.filter(delete_flag=0, tag=tag)
    else:
        if not tag:
            article_list = models.BlogArticle.objects.filter(delete_flag=0, title__icontains=search)
            tag = '全部'
        else:
            if tag == '全部':
                article_list = models.BlogArticle.objects.filter(delete_flag=0, title__icontains=search)
            else:
                tag = request.GET.get('tag')
                article_list = models.BlogArticle.objects.filter(delete_flag=0, tag=tag, title__icontains=search)

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
                coin = userinfo.fengyacoin
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
                        fengyacoin = acticlejudge.articlecost
                        if userinfo.fengyacoin < fengyacoin:
                            situation = 3
                            return render(request, 'articletran.html',
                                          {"currentPage": currentPage, 'situation': situation})
                        else:
                            fengyacoin = userinfo.fengyacoin - fengyacoin
                            models.Commonuser.objects.filter(userid=username).update(fengyacoin=fengyacoin)
                            coin = fengyacoin
                    new_data = models.ArticleContain.objects.create(title=titlename,userid=username)
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

    #获取该文章评论列表
    commitlist = models.ArticleContain.objects.filter(title=titlename,commentflag=2).order_by('firstreaddate')


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
                userbalance = fengyacoin - int(cost)

            if userbalance >= 0:
                try:
                    if filecosttype == 1:
                        userinfo.integrate = userbalance
                        userinfo.save()
                    elif filecosttype == 2:
                        userinfo.fengyacoin = userbalance
                        userinfo.save()

                    models.Fileright.objects.create(userid=userid, title=titlename)
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
                    last = userinfo.fengyacoin

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
        username = request.session['user_id']
        commitcontent = request.POST.get("commitcontent")

        try:
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

