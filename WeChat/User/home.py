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
from .forms import Activeform
from .forms import RealNameform
from .forms import BankBindform
from .forms import BankCashform
from django.forms.models import model_to_dict
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.http import urlquote
from django.http import JsonResponse
from django.db.models import Q
from django.db.models import F
from itertools import chain

from User.emailsend import get_user_pravite_key
from User.emailsend import random_str  # 用于生成随机码
from User.emailsend import send_code_email  # 用于生成随机码
from User.emailsend import judege_spread_level
from User.emailsend import judege_spread_precent
from User.emailsend import get_active_spread_precent
from User.emailsend import next_spread_level_value
from User.emailsend import verifycode
from User.emailsend import ScreenAppid

from User.wechatpay import order_num
from User.wechatpay import cash_num
from User.wechatpay import opratecoinpool
from User.wechatpay import replace_username
from User.wechatpay import get_md5
from User.wechatpay import get_spreadqrcode
from User.wechatpay import replace_realname
from User.wechatpay import replace_cardid
from User.wechatpay import judge_cardid
from User.wechatpay import wechatauthorizeqrcode
from User.wechatpay import get_bindwechat_userinfo
from User.wechatpay import isequaldate
from User.wechatpay import get_authorize_url_qrcode
from User.wechatpay import get_authorize_url_article_qrcode
from User.wechatpay import call_back_authorize_qrcode

def loginverify(func):#登陆验证装饰器
    def inner(request):
        if not request.session.get('is_login', None):
            return redirect('/index/')

        model = request.session['model']
        if model != 1000:
            return redirect("/logout/")
        return func(request)

    return inner

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

   md5 = request.GET.get('md5',"")
   #设置cookie


   if not request.session.get('is_login', None):
       response = render(request, 'index.html', locals())
       response.set_cookie("md5",md5,expires=None)
       return response

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
                    request.session['isspread'] = user.isspread
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

            if username.isalnum() == False:
                message = "用户名只能包含字母和数字，不能包含汉字及其他字符，请重新编写后，再进行注册！"
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
                new_user.identify = phonenumber

                md5 = request.COOKIES.get('md5',"")
                binduser_list = []
                binduser_list = models.Commonuser.objects.filter(md5=md5)

                if len(md5) <= 0 | binduser_list.count() == 0:
                    new_user.acountuser = 'webregister'
                    new_user.source = 'webregister'
                else:
                    new_user.acountuser = 'wechat'
                    new_user.source = 'wechat'
                    new_user.binduser = md5
                    binddate = timezone.now().strftime("%Y-%m-%d")
                    new_user.binddate = binddate
                new_user.save()
                response = render(request, 'registertran.html') # 自动跳转到登录页面
                response.delete_cookie('md5')
                return response

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
        giftcoin = int(User.giftcoin/100)
        isbind = 0
        isalready = -1
        qrcodeurl = ""
        qrcodepath = ""
        binduser = User.binduser

        if len(binduser) > 0:
            isbind = 1

        active_form = Activeform()

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

        #获取每日关注公众号信息
        #判断今日是否获取过，或者已领取过缝芽币
        fengyadate = User.fengyadate
        appstate = User.appstate
        appid = User.appid
        if(isequaldate(fengyadate) == 1):
            isalready = 1
        else:
            if appstate == 1:
                isalready = 0
            else:
                result,appidget = ScreenAppid(username)
                if result == 0:
                    User.appstate = 1
                    User.appid = appidget
                    User.save()
                    appid = appidget
                    isalready = 0
                elif result == 2:
                    isalready = 2
                elif result == -1:
                    isalready = -1

        if isalready == 0:
            # 获取公众号二维码及授权二维码
            qrcodeurl = models.AuthorizeInfo.objects.get(appid=appid).value(qrcodeurl)
            qrcodepath = get_authorize_url_qrcode(appid,username)

        return render(request, 'userinfoshow.html', locals())
    except:
        return render(request, 'commontran.html')


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
    showgiftcoin = 0
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
                        userfycoin = userinfo.fengyacoin
                        giftcoin = userinfo.giftcoin
                        totalcoin = userfycoin + giftcoin
                        if totalcoin < fengyacoin:
                            situation = 3
                            return render(request, 'articletran.html',
                                          {"currentPage": currentPage, 'situation': situation})
                        else:
                            if giftcoin >= fengyacoin:
                                showgiftcoin = giftcoin - fengyacoin
                                models.Commonuser.objects.filter(userid=username).update(giftcoin=showgiftcoin)
                            elif giftcoin == 0:
                                opratecoinpool(fengyacoin)
                                coin = userinfo.fengyacoin - fengyacoin
                                models.Commonuser.objects.filter(userid=username).update(fengyacoin=coin)
                            else:
                                decreasenum = fengyacoin - giftcoin
                                coin = userfycoin - decreasenum
                                opratecoinpool(decreasenum)
                                models.Commonuser.objects.filter(userid=username).update(fengyacoin=coin, giftcoin=0)

                            showgiftcoin = showgiftcoin/100
                            coin = coin/100

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
            giftcoin = userinfo.giftcoin
            articleblog = models.BlogArticle.objects.get(title=titlename)
            filecosttype = articleblog.filecosttype
            cost = articleblog.cost
            userbalance = 0
            if filecosttype == 1:
                userbalance = intergrate - int(cost)
            elif filecosttype == 2:
                userbalance = fengyacoin + giftcoin - int(cost)*100

            if userbalance >= 0:
                try:
                    if filecosttype == 1:
                        userinfo.integrate = userbalance
                        userinfo.save()
                    elif filecosttype == 2:
                        #消耗,优先消耗赠送逢芽币
                        if giftcoin >= int(cost)*100:
                            giftcoinnum = giftcoin - int(cost)*100
                            userinfo.giftcoin = giftcoinnum
                            userinfo.save()
                        elif giftcoin == 0:
                            opratecoinpool(int(cost) * 100)
                            userinfo.fengyacoin = userbalance
                            userinfo.save()
                        else:
                            decreasenum = int(cost)*100 - giftcoin
                            realnum = fengyacoin - decreasenum
                            opratecoinpool(decreasenum)
                            userinfo.fengyacoin = realnum
                            userinfo.giftcoin = 0
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


@loginverify
def orderlist(request):
    kind = 0

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

@loginverify
def ajax_apeal(request):#申诉用post
    kind = 0

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

@loginverify
def spreaduorderlist(request):
    kind = 0
    contentname = "订单分成列表"
    order_list = []
    username = request.session['user_id']
    type = int(request.GET.get('type',3))
    try:
        User = models.Commonuser.objects.get(userid=username)

        md5 = User.md5

        if len(md5) <= 0:
            info = "您还未激活成为分销用户，请激活后再试！"
            return render(request, 'commoninfotran.html',{"info":info})

        order_list = models.OrderOver.objects.filter(binduser=md5,orderstate=1).order_by('-chargedate')

        nNum = 0
        for order in order_list:
            replacename = replace_username(order.userid)
            order_list[nNum].userid = replacename
            ++nNum
    except:
        return render(request, 'commontran.html')

    paginator = Paginator(order_list, 15)
    # 从前端获取当前的页码数,默认为1
    page = request.GET.get('page', 1)

    currentPage = int(page)

    try:
        order_list = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        order_list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        order_list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容

    return render(request, 'spreadorderlist.html',locals())

@loginverify
def spreadbindlist(request):
    kind = 0
    contentname="绑定信息"
    user_list = []
    username = request.session['user_id']
    type = int(request.GET.get('type',2))
    try:
        User = models.Commonuser.objects.get(userid=username)

        md5 = User.md5

        if len(md5) <= 0:
            info = "您还未激活成为分销用户，请激活后再试！"
            return render(request, 'commoninfotran.html',{"info":info})

        user_list = models.Commonuser.objects.filter(binduser=md5).order_by('-binddate')

        nNum = 0
        for userreplace in user_list:
            replacename = replace_username(userreplace.userid)
            user_list[nNum].userid = replacename
            ++nNum
    except:
        return render(request, 'commontran.html')

    paginator = Paginator(user_list, 15)
    # 从前端获取当前的页码数,默认为1
    page = request.GET.get('page', 1)

    #if int(page) > article_list.count()/10:
       # raise Http404("Page does not exist")
    # 把当前的页码数转换成整数类型
    currentPage = int(page)

    try:
        user_list = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        user_list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        user_list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容

    return render(request, 'spreadbindlist.html',locals())

@loginverify
def ActivateSpread(request):
    kind = 0
    username = request.session['user_id']
    type = 1
    contentname = "推广用户信息"
    activatecode = ""
    spreadprecent = 5

    if request.method == "POST":
        activatecode = request.POST["activatecode"]
        if len(activatecode) > 0:
            spreadprecent = get_active_spread_precent(activatecode,username)
            if spreadprecent == 1:
                info = "您的认证激活码已使用，请联系我们重新获取，给您带来的困扰我们深表歉意！"
                return render(request, 'commoninfotran.html', {"info": info})
            elif spreadprecent == 0:
                info = "您的认证激活码无效，请联系我们重新获取，给您带来的困扰我们深表歉意！"
                return render(request, 'commoninfotran.html', {"info": info})
    else:
        info = "暂未开通非认证分销用户激活，请联系我们获得认证激活码！"
        return render(request, 'commoninfotran.html', {"info": info})

    try:
        User = models.Commonuser.objects.get(userid=username)
        md5 = get_md5(username)
        User.md5 = get_md5(username)
        spreadurl = "www.yuntaoz.cn/?md5=" + md5
        qrcodepath = get_spreadqrcode(spreadurl,username)

        if len(qrcodepath) == 0:
            info = "您的推广二维码未生成成功，请重新申请，给您带来的困扰我们深表歉意！"
            return render(request, 'commoninfotran.html', {"info": info})

        User.spreadcode = get_user_pravite_key()
        User.spreadprecent = spreadprecent
        User.isspread = 1
        User.isaccount = 1
        level = 1
        nextlevel = 50
        User.save()
    except:
        return render(request, 'commontran.html')

    request.session['isspread'] = 1
    return redirect("/spreadinfo/")


@loginverify
def ShowSpreadInfo(request):
    kind = 0
    username = request.session['user_id']
    type = 1
    contentname = "推广用户信息"
    try:
        User = models.Commonuser.objects.get(userid=username)
        md5 = User.md5

        if len(md5) <= 0:
            info = "您还未激活成为分销用户，请激活后再试！"
            return render(request, 'commoninfotran.html',{"info":info})

        qrcode_name = username + '.png'
        qrcodepath = '/spreadqrcode/' + qrcode_name

        level = judege_spread_level(User.totalmeony)

        nextlevel = next_spread_level_value(level)

    except:
        return render(request, 'commoninfotran.html', {"info": info})

    return render(request, 'spreaduserinfo.html', locals())

@loginverify
def bind(request):

    username = request.session['user_id']
    if request.method == "POST":
        code = request.POST["code"]
        try:
            binduser = models.Commonuser.objects.get(spreadcode=code)
            md5 = binduser.md5

            User = models.Commonuser.objects.get(userid=username)
            User.binduser = md5
            User.integrate += 300
            User.save()

        except:
            return render(request, 'commontran.html')
    else:
        return render(request, 'commontran.html')

    return render(request, 'bindtran.html')

@loginverify
def invite(request):
    username = request.session['user_id']
    if request.method == "POST":
        activatecode = request.POST["code"]
        try:
            User = models.Commonuser.objects.get(userid=username)
            spreadprecent = 5
            if User.isspread == 1:
                if len(activatecode) > 0:
                    spreadprecent = get_active_spread_precent(activatecode, username)
                    if spreadprecent == 1:
                        info = "您的认证激活码已使用，请联系我们重新获取，给您带来的困扰我们深表歉意！"
                        return render(request, 'commoninfotran.html', {"info": info})
                    elif spreadprecent == 0:
                        info = "您的认证激活码无效，请联系我们重新获取，给您带来的困扰我们深表歉意！"
                        return render(request, 'commoninfotran.html', {"info": info})
                else:
                    return render(request, 'commontran.html')

                if User.spreadprecent < spreadprecent:
                    User.spreadprecent = spreadprecent
                    User.isaccount = 1
                    User.save()
                else:
                    spreadprecent = User.spreadprecent
            else:
                return render(request, 'commontran.html')

        except:
            return render(request, 'commontran.html')
    else:
        return render(request, 'commontran.html')

    return render(request, 'invitetran.html', locals())

@loginverify
def real(request):
    kind = 0
    username = request.session['user_id']
    User = models.Commonuser.objects.get(userid=username)

    if request.method == "POST":
        realname = request.POST["realname"]
        cardid = request.POST["cardid"]

        if judge_cardid(cardid):
            User.realname = realname
            User.cardid = cardid
            User.save()
            info = "您已正确填写实名认证信息！"
            return render(request, 'realtran.html', locals())
        else:
            info = "您的身份信息填写有误，请重新填写！"
            return render(request, 'realtran.html', locals())

    realjudge = User.realname
    content="实名认证"
    type = 4
    if len(realjudge) > 0:
        isreal = True
        realname_whole = User.realname
        cardid_whole = User.cardid
        realname = replace_realname(realname_whole)
        cardid = replace_cardid(cardid_whole)
        return render(request, 'spreadrealname.html', locals())
    else:
        isreal = False
        realname_form = RealNameform()
        return render(request, 'spreadrealname.html', locals())

@loginverify
def bindbank(request):
    username = request.session['user_id']

    content = "银行卡提现"
    type = 6
    kind = 0
    totalmeony = 0
    bankid = ""
    bankname = ""
    if request.method == "POST":
        #n拿出数据
        try:
            bankid = request.POST["bankid"]
            bankname = request.POST["bankname"]
            code = request.POST["code"]
            # 拿出User
            User = models.Commonuser.objects.get(userid=username)
            totalmeony = User.spreadmeony
            if len(User.realname) == 0:
                info = "请先实名认证，再进行操作！"
                return render(request, 'commoninfotran.html', {"info": info})

            email = User.identify

            # 判定验证码
            result = verifycode(code,2,email)

            if result == 0:
                info = "请先获取验证码，再进行操作！"
                return render(request, 'commoninfotran.html', {"info": info})
            elif result == -1:
                info = "您的验证码已超时，请重新获取，再进行操作！"
                return render(request, 'commoninfotran.html', {"info": info})

            # 写入数据库
            try:
                Bank = models.CashBind.objects.get(userid=username)
                Bank.bankid = bankid
                Bank.bankname = bankname
                Bank.save()
            except:
                try:
                    Bank = models.CashBind.objects.create(userid=username, bankid=bankid, bankname=bankname)
                    Bank.save()
                except:
                    info = "未成功绑定银行卡，请您稍后再试，若一直无法绑定请联系客服,邮箱fengyadata@163.com！"
                    return render(request, 'commoninfotran.html', {"info": info})
            banktimes = 2
            bankbind_form = BankBindform()
            bankcash_form = BankCashform()
            isbank = True
            return render(request, 'spreadbankcash.html', locals())
        except:
            return render(request, 'commontran.html')
    else:
        try:
            User = models.Commonuser.objects.get(userid=username)
            totalmeony = User.spreadmeony
            if len(User.realname) == 0:
                info = "请先实名认证，再进行操作！"
                return render(request, 'commoninfotran.html', {"info": info})
        except:
            return render(request, 'commontran.html')

        isbank = False
        banktimes = 0
        try:
            Bank = models.CashBind.objects.get(userid=username)
            bankid = Bank.bankid
            bankname = Bank.bankname
            banktimes = Bank.banktimes
            isbank = True
        except:
            isbank = False

        bankbind_form = BankBindform()
        bankcash_form = BankCashform()
        return render(request, 'spreadbankcash.html', locals())


@loginverify
def bankcash(request):
    content = "银行卡提现"
    kind = 0
    if request.method != "POST":
        return render(request, 'commontran.html')

    try:
        username = request.session['user_id']
        bankid = ""
        bankname = ""
        cash = float(request.POST["cash"])*100
        code = request.POST["code"]

        User = models.Commonuser.objects.get(userid=username)

        if len(User.realname) == 0:
            info = "请先实名认证，再进行操作！"
            return render(request, 'commoninfotran.html', {"info": info})

        email = User.identify
        balance = User.spreadmeony
        realname = User.realname

        if balance < cash:
            info = "余额不足，请重新操作！"
            return render(request, 'commoninfotran.html', {"info": info})

        # 判定验证码
        result = verifycode(code, 1, email)

        if result == 0:
            info = "请先获取验证码，再进行操作！"
            return render(request, 'commoninfotran.html', {"info": info})
        elif result == -1:
            info = "您的验证码已超时，请重新获取，再进行操作！"
            return render(request, 'commoninfotran.html', {"info": info})

        try:
            try:
                Bank = models.CashBind.objects.get(userid=username)
                if Bank.banktimes <= 0:
                    info = "银行卡提现次数本月已达上限，请下一月一号早上九点以后重试！"
                    return render(request, 'commoninfotran.html', {"info": info})

                bankid = Bank.bankid
                bankname = Bank.bankname
                Bank.banktimes = Bank.banktimes - 1
                Bank.save()
            except:
                info = "您尚未绑定银行卡，请绑定后再进行操作！"
                return render(request, 'commoninfotran.html', {"info": info})
            # 先扣钱
            User.spreadmeony = F('spreadmeony') - cash
            User.save()
            # 创建提现订单
            orderid = cash_num("20", username)
            cashorder = models.CashOrder.objects.create(orderid=orderid, userid=username, meony=cash,
                                                        bankid=bankid, bankname=bankname, orderstate=2,
                                                        realname=realname, appeal=-1, email=email)
            cashorder.save()
            info = "恭喜您，提现订单创建成功，我们会在5个工作日内处理您的提现订单，请到银行卡提现记录中查看订单状态！"
            return render(request, 'cashtran.html', {"info": info})
        except:
            info = "对不起，您的提现操作未成功，请稍后重试！"
            return render(request, 'commoninfotran.html', {"info": info})


    except:
        return render(request, 'commontran.html')



@loginverify
def ajax_getcashcode(request):#获取提现激活码
    #type 1现金提现，2：绑定银行卡
    if request.method == "POST":
        try:
            username = request.session['user_id']
            type = int(request.POST["type"])
            User = models.Commonuser.objects.get(userid=username)
            email = User.identify
            md5 = User.md5
            if len(md5) <= 0:
                info = "您尚未激活推广人权限，请激活后重试！"
                return render(request, 'commoninfotran.html', {"info": info})

            if len(email) == 0:
                return JsonResponse(0, safe=False)

            str = random_str()

            try:
                code = models.CashCode.objects.get(email=email)
                code.codeid = str
                code.type = type
                code.save()
            except:
                try:
                    code = models.CashCode.objects.create(email=email, codeid=str, type=type)
                    code.save()
                except:
                    return JsonResponse(0, safe=False)

            if type == 1:
                if send_code_email(email, str, "cash"):
                    return JsonResponse(1, safe=False)
                else:
                    return JsonResponse(0, safe=False)
            elif type == 2:
                if send_code_email(email, str, "bindbank"):
                    return JsonResponse(1, safe=False)
                else:
                    return JsonResponse(0, safe=False)

        except:
            return JsonResponse(-1, safe=False)
    else:
        return JsonResponse(0, safe=False)

@loginverify
def bankcashlist(request):
    kind = 0
    content = "银行卡提现记录"
    type = 8
    username = request.session['user_id']
    order_list = []

    try:
        order_list = models.CashOrder.objects.filter(userid=username, iswechat=0).order_by('-time')
    except:
        info = "系统参数错误，请稍后重试！"
        return render(request, 'commoninfotran.html', {"info": info})

    paginator = Paginator(order_list, 15)
    # 从前端获取当前的页码数,默认为1
    page = request.GET.get('page', 1)

    currentPage = int(page)

    try:
        order_list = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        order_list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        order_list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容

    try:
        User = models.Commonuser.objects.get(userid=username)
        return render(request, 'bankcashlist.html', locals())
    except:
        info = "系统参数错误，请稍后重试！"
        return render(request, 'commoninfotran.html', {"info": info})


@loginverify
def ajax_spreadapeal(request):#申诉用post
    username = request.session['user_id']

    if request.method == "POST":
        orderid = request.POST["orderid"]
        try:
            models.CashOrder.objects.filter(userid=username, orderid=orderid).update(appeal=1)
            return JsonResponse(1, safe=False)
        except:
            return JsonResponse(-1, safe=False)

    return JsonResponse(-1, safe=False)

@loginverify
def wechatcashlist(request):
    kind = 0
    content = "微信提现记录"
    type = 7
    username = request.session['user_id']
    order_list = []

    try:
        order_list = models.CashOrder.objects.filter(userid=username, iswechat=1).order_by('-time')
    except:
        info = "系统参数错误，请稍后重试！"
        return render(request, 'commoninfotran.html', {"info": info})

    paginator = Paginator(order_list, 15)
    # 从前端获取当前的页码数,默认为1
    page = request.GET.get('page', 1)

    currentPage = int(page)

    try:
        order_list = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        order_list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        order_list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容

    try:
        User = models.Commonuser.objects.get(userid=username)
        return render(request, 'wechatcashlist.html', locals())
    except:
        info = "系统参数错误，请稍后重试！"
        return render(request, 'commoninfotran.html', {"info": info})

@loginverify
def wechatcash(request):
    type=5
    content = "微信提现"
    kind = 0
    username = request.session['user_id']
    realname = ""
    email = ""
    balance = ""
    isbind = False
    iswechatid = False
    wechatid = ""
    openid = ""
    daytimes = 0
    monthtimes = 0
#推广账户及实名认证验证
    try:
        User = models.Commonuser.objects.get(userid=username)
        realname = User.realname
        email = User.identify
        balance = User.spreadmeony

        md5 = User.md5
        if len(md5) <= 0:
            info = "您尚未激活推广人权限，请激活后重试！"
            return render(request, 'commoninfotran.html', {"info": info})

        if len(User.realname) == 0:
            info = "请先实名认证，再进行操作！"
            return render(request, 'commoninfotran.html', {"info": info})

    except:
        info = "数据获取失败，请稍后再试！"
        return render(request, 'commoninfotran.html', {"info": info})

#微信号绑定验证
    try:
        BindUser = models.CashBind.objects.get(userid=username)
        wechatid = BindUser.wechatid
        openid = BindUser.openid
        if len(openid) != 0:
            isbind = True

        if len(wechatid) != 0:
            iswechatid = True

        daytimes = BindUser.wechateverydaytimes
        monthtimes = BindUser.wechattimes
    except:
        wechatid = ""

    qrcodepath = wechatauthorizeqrcode(username)

    if request.method == "POST":
        try:
            wechatid = request.POST["wechatid"]
            cash = float(request.POST["cash"]) * 100
            code = request.POST["code"]

            BindUserOprate = models.CashBind.objects.get(userid=username)
            if BindUserOprate.wechateverydaytimes <= 0:
                info = "今日提现次数已达上限，请于明日9点以后重试！"
                return render(request, 'commoninfotran.html', {"info": info})

            if BindUserOprate.wechattimes <= 0:
                info = "本月提现次数已达上限，请下一个月一号9点以后重试！"
                return render(request, 'commoninfotran.html', {"info": info})

            if balance < cash:
                info = "余额不足，请重新操作！"
                return render(request, 'commoninfotran.html', {"info": info})

            # 判定验证码
            result = verifycode(code, 1, email)

            if result == 0:
                info = "请先获取验证码，再进行操作！"
                return render(request, 'commoninfotran.html', {"info": info})
            elif result == -1:
                info = "您的验证码已超时，请重新获取，再进行操作！"
                return render(request, 'commoninfotran.html', {"info": info})

            #开始生成提现订单
            try:
                # 先扣钱
                UserOprate = models.Commonuser.objects.get(userid=username)
                UserOprate.spreadmeony = F('spreadmeony') - cash
                UserOprate.save()
                #减次数
                BindUserOprate.wechateverydaytimes = BindUserOprate.wechateverydaytimes - 1;
                BindUserOprate.wechattimes = BindUserOprate.wechattimes - 1;
                BindUserOprate.save()
                # 创建提现订单
                orderid = cash_num("10", username)
                cashorder = models.CashOrder.objects.create(orderid=orderid, userid=username, meony=cash,
                                                            iswechat=1,realname=realname, appeal=-1, email=email,
                                                            openid=openid,wechatid=wechatid,orderstate=2)
                cashorder.save()
                return render(request, 'cashwechattran.html',{"orderid":orderid})
            except:
                info = "对不起，您的提现操作未成功，请稍后重试！"
                return render(request, 'commoninfotran.html', {"info": info})

        except:
            return render(request, 'commontran.html')
    else:
        return render(request, 'spreadwechatcash.html', locals())

def wechatbind(request):
    code = request.GET.get('code',"")
    userid = request.GET.get('state',"")

    if len(code) == 0 | len(userid) == 0:
        return HttpResponse("微信返回参数错误，请重新扫码绑定")

    return render(request, 'bindwechat.html', locals())

def wechatverify(request):
    if request.method == "POST":
        code = request.POST['code', ""]
        userid = request.POST['state', ""]
        wechatid = request.POST['wechatid', ""]
        iswechatid = False
        if len(code) == 0 | len(userid) == 0:
            return HttpResponse("微信返回参数错误，请重新扫码绑定")

        if len(wechatid) > 0:
            iswechatid = True

        userinfodict = get_bindwechat_userinfo(code)
        errorcode = userinfodict.get("errorcode")

        if errorcode < 0:
            return HttpResponse(userinfodict.get("errormessage"))

        try:
            User = models.Commonuser.objects.get(userid=userid)
            realname = User.realname
            md5 = User.md5

            if len(realname) == 0:
                success = 0
                info = "您所绑定的用户尚未实名认证，请实名认证后重试"
                return render(request, 'wechatbindtran.html', locals())

            if len(md5) == 0:
                success = 0
                info = "您所绑定的用户尚未激活推广账户，请激活后重试"
                return render(request, 'wechatbindtran.html', locals())

            try:
                BindUser = models.CashBind.objects.get(userid=userid)
                BindUser.openid = userinfodict.get("openid")
                BindUser.wechatid = wechatid
                BindUser.save()
                success = 1
                return render(request, 'wechatbindtran.html', locals())
            except:
                try:
                    BindUser = models.CashBind.objects.create(userid=userid,openid=userinfodict.get("openid"),wechatid=wechatid)
                    BindUser.save()
                    success = 1
                    return render(request, 'wechatbindtran.html', locals())
                except:
                    success = 0
                    info = "很抱歉，服务器写入数据失败，请稍后重新扫码绑定！"
                    return render(request, 'wechatbindtran.html', locals())
        except:
            success = 0
            info = "您所绑定的用户不存在，请注册后重试"
            return render(request, 'wechatbindtran.html', locals())
    else:
        return HttpResponse("提交参数有误，请重新扫码绑定")

@loginverify
def ajax_checkcash(request):
    orderid = request.GET.get("orderid","")

    try:
        order = models.CashOrder.objects.get(orderid=orderid)
        orderstate = order.orderstate
        return JsonResponse(orderstate, safe=False)
    except:
        return JsonResponse(-1, safe=False)

@loginverify
def cashresult(request):
    result = int(request.GET.get("result",0))
    content = ""
    failreason = ""

    if result == 1:
        content = "提现成功！"
    elif result == 0:
        content = "提现失败！"
        orderid = request.GET.get("orderid","")
        try:
            order = models.CashOrder.objects.get(orderid=orderid)
            if order.usererror == 1:
                failreason = order.failreason
            else:
                failreason = "系统错误,请稍后重试"
        except:
            failreason = "系统错误，或订单不存在，请稍后再试"
    elif result == -1:
        ontent = "提现订单状态不明！"
    elif result == 3:
        ontent = "提现订单处理中...！"

    return render(request, 'wechatcashresult.html', locals())

@loginverify
def authorizeinfo(request):
    type = 9
    userid = request.session['user_id']
    isauthorize = False
    User = models.Commonuser.objects.get(userid=userid)

    try:
        authorize = models.AuthorizeInfo.objects.get(userid=userid, type=1)
        nickname = authorize.nick_name
        servicetype = authorize.service_type
        principal = authorize.principal
        headurl = authorize.head_img
        qrcodeurl = authorize.qrcode_url
        describe = authorize.describe
        isauthorize = True
        return render(request, 'wechatauhoorize/authorize.html', locals())
    except:
        success, qrcodepath = call_back_authorize_qrcode(userid)
        return render(request, 'wechatauhoorize/authorize.html', locals())

#def update_authorize_info(request):公众号信息腾讯不可改，暂不支持更新信息

@loginverify
def authorizenocase(request):#关注公众号免费阅读文章
    userid = request.session['user_id']
    title = request.GET.get("title", "")
    currentPage = int(request.GET.get('currentPage',1))

    if len(title) == 0:
        return render(request, 'commontran.html', locals())

    isalready = 0
    appid = ""
    try:
        arcticlecontain = models.ArticleContain.objects.get(title=title, userid=userid)
        isalready = 1
    except:
        result, appid = ScreenAppid(userid)
        if result == 0:
            isalready = 0
        elif result == 2:
            isalready = 2
        elif result == -1:
            isalready = -1


    if isalready == 0:
        # 获取公众号二维码及授权二维码
        qrcodeurl = models.AuthorizeInfo.objects.get(appid=appid).value(userid)
        qrcodepath = get_authorize_url_article_qrcode(appid, userid,title)

    return render(request, 'wechatauhoorize/authorizenocase.html', locals())

@loginverify
def ajax_checkarticle(request):
    userid = request.session['user_id']
    title = request.GET.get('title',"")

    result = -1
    try:
        articlecontain = models.ArticleContain.objects.get(userid=userid,title=title)
        if articlecontain.costtype == 5:
            result = 1
        result = 1
    except:
        result = -1

    return JsonResponse(result, safe=False)

@loginverify
def allconcernarticle(request):
    userid = request.session['user_id']
    title = request.GET.get("title", "")
    currentPage = int(request.GET.get('currentPage', 1))

    if ScreenAppid(userid) != 2:
        info = "对不起，您尚未关注所有公众号，无法开通！"
        return render(request,"commoninfotran.html",{"info":info})

    try:
        arcticlecontain = models.ArticleContain.objects.get(title=title, userid=userid)
        if not arcticlecontain:
            article = models.BlogArticle.objects.get(title=title)
            new_data = models.ArticleContain.objects.create(title=title, userid=userid,
                                                            costtype=article.articlecosttype,
                                                            cost=0, tag=article.tag)
            new_data.save()
            url = "articlecontent/?title=" + title + "&currentPage=" + str(currentPage)
            return redirect(url)
    except:
        return render(request,"commontran.html")

@loginverify
def allconcerncoin(request):
    userid = request.session['user_id']

    if ScreenAppid(userid) != 2:
        info = "对不起，您尚未关注所有公众号，无法开通！"
        return render(request, "commoninfotran.html", {"info": info})
    # 处理领取缝芽币，防止以重复领取，用户界面勿忘领取过不在显示二维码
    try:
        User = models.Commonuser.objects.get(userid=userid)
        giftdate = User.fengyadate
        if len(giftdate) != 0:
            alreadyget = isequaldate(giftdate)
            if alreadyget == 1:
                return render(request, 'authorizeuserresult.html', {"sign": -2})

        # 赠送缝芽币不进入pool，但是有订单生成，表示赠送
        # 赠送
        User.fengyadate = timezone.now().strftime("%Y-%m-%d")
        User.giftcoin = F('giftcoin') + 500
        User.save()
    except:
        return render(request, 'authorizeuserresult.html', {"sign": -3})

    try:
        # 生成赠送订单（积分赠送也要生成）,102赠送逢芽币
        orderid = order_num(102, userid)
        order = models.OrderOver.objects.create(orderid=orderid, coin=500, userid=userid, orderstate=2, appeal=-1)
        order.save()
    except:
        pass

    return render(request, 'authorizeuserresult.html', {"sign": 1})


def tranupdate(request):
    return render(request,"Tran/updatetran.html")

def ce(request,id):
    result = request.GET.get("result")
    isalready = 2
    filepath = os.path.join("\\wechatauhoorize", "authorizenocase.html")
    return render(request,"wechatauhoorize/authorizenocase.html", locals())
