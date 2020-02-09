import os
import re
from django.db.models import Max
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from User import models
from User.forms import UserForm
from User.forms import ArticleForm
from User.forms import CenterForm
from User.forms import ActiveCodeform

from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from User.emailsend import get_active_code
from django.db.models import F

def loginverify(func):#登陆验证装饰器
    def inner(request):
        if not request.session.get('is_login', None):
            return redirect('/superindex/')

        model = request.session['model']
        if model != 1001:
            return redirect("/superlogout/")
        return func(request)

    return inner

def iframe(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/superindex/")

    model = request.session['model']
    if model != 1001:
        return redirect("/superlogout/")

    keypath=articletitle = request.GET.get('key')

    if not keypath:
        raise Http404("html does not exist")

    filepath=os.path.join("C:\\centerdata", keypath)
    return render(request, filepath)

def showdata(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/superindex/")

    model = request.session['model']
    if model != 1001:
        return redirect("/superlogout/")

    kind = 1

    message = 1

    datelist=[]
    SSEList=[]
    trendlist=[]
    SSEListOne = []
    simSSElistOne=[]
    SSEOne=1
    simSSEOne=1
    if request.method == "POST":
        iddate = request.POST["inputdate"]
        if iddate:
            try:
                message = 2
                centerdata = models.CenterData.objects.get(date=iddate)
                trend=centerdata.trend
                judge=centerdata.judge
                valueone=centerdata.valueone
                valuetwo=centerdata.valuetwo
                keypath=centerdata.filepath
                dateinit=iddate
                data_list = models.CenterData.objects.filter(date__lte=dateinit).order_by('-date')
                size = len(data_list)
                if size > 29:
                    SSEOne = data_list[29].valueone
                    simSSEOne = data_list[29].valuetwo
                    for i in range(0,30):
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

                        ssedict={'y':data_list[i].valueone,'color':color}
                        SSEList.append(ssedict)
                        trendlist.append(data_list[i].trend)
                        SSEListOne.append(round(data_list[i].valueone / SSEOne,2))
                        simSSElistOne.append(round(data_list[i].valuetwo / simSSEOne,2))

                datelist.reverse();
                SSEList.reverse();
                trendlist.reverse();
                SSEListOne.reverse();
                simSSElistOne.reverse();

                if len(judge) > 0:
                    text = judge
                    return render(request, 'showdata.html', locals())

                return render(request, 'showdata.html', locals())
            except:
                message = 0

    #选择日期当天无数据，或者刚进入Get，获取最近一天数据显示

    centerdata = models.CenterData.objects.all().order_by("-date")[0]

    if message != 0:
        datesel = request.GET.get('dateselect')
        centerdata = models.CenterData.objects.get(date=datesel)
   # else:
       # centerdata = models.CenterData.objects.all().aggregate(Max('date'))


    trend = centerdata.trend
    judge = centerdata.judge
    valueone = centerdata.valueone
    valuetwo = centerdata.valuetwo
    keypath = centerdata.filepath
    dateinit=centerdata.date
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
        return render(request, 'showdata.html', locals())

    return render(request, 'showdata.html', locals())


def centerdatamanage(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/superindex/")

    model = request.session['model']
    if model != 1001:
        return redirect("/superlogout/")

    kind = 1
    data_list = []
    startdate = ""
    enddate = ""
    managemodel = 0

    if request.method == "POST":
    # 日期筛选
        startdate = request.POST["startdate"]
        enddate = request.POST["enddate"]
        try:
            data_list = models.CenterData.objects.filter(date__range=(startdate,enddate))
        except:
            managemodel = -1
    else:
        data_list = models.CenterData.objects.all()


    paginator = Paginator(data_list, 15)
    # 从前端获取当前的页码数,默认为1
    page = request.GET.get('page', 1)

    # if int(page) > article_list.count()/10:
    # raise Http404("Page does not exist")
    # 把当前的页码数转换成整数类型
    currentPage = int(page)

    try:
        data_list = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        data_list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        data_list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容

    return render(request, 'centerdatamanage.html',locals())

def centerdatadelete(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/superindex/")

    model = request.session['model']
    if model != 1001:
        return redirect("/superlogout/")

    kind = 1
    centerdatadate = request.GET.get('datadelete')
    models.CenterData.objects.filter(date=centerdatadate).delete()

    return redirect("/datamanage/")




def centerdatamodify(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/superindex/")

    model = request.session['model']
    if model != 1001:
        return redirect("/superlogout/")

    kind = 1

    if request.method == "POST":
        CenterData_form = CenterForm(request.POST)
        message = 0

        if CenterData_form.is_valid():

            myFile = request.FILES.get("myfile", None)
            if not myFile:
                message = -2

            if message != -2:
                if not myFile.name.endswith(".html"):
                    message = -2


            iddate = request.POST["inputdate"]
            trend = CenterData_form.cleaned_data['trend']
            judge = CenterData_form.cleaned_data['judge']
            valueone = CenterData_form.cleaned_data['valueone']
            valuetwo = CenterData_form.cleaned_data['valuetwo']
            try:
                centerdata = models.CenterData.objects.get(date=iddate)

                if message != -2:
                    message = 1
                    filename = iddate + ".html"
                    destination = open(os.path.join("C:\\django-shares-plat\\WeChat\\templates\\centerdata", filename),
                                       'wb+')  # 打开特定的文件进行二进制的写操作
                    for chunk in myFile.chunks():  # 分块写入文件
                        destination.write(chunk)
                    destination.close()
                    centerdata.filepath = filename
                #os.remove(os.path.join("C:\\centerdata", filename))

                centerdata.valueone = valueone
                centerdata.valuetwo = valuetwo
                centerdata.judge = judge
                centerdata.trend = trend
                centerdata.save()
                CenterData_form = CenterForm(locals())
                return render(request,  'centerdatamodify.html', locals())
            except:


                if message == -2:
                    message = -3
                    return render(request, 'centerdatamodify.html', locals())

                filename = iddate + ".html"
                destination = open(os.path.join("C:\\django-shares-plat\\WeChat\\templates\\centerdata", filename), 'wb+')  # 打开特定的文件进行二进制的写操作
                for chunk in myFile.chunks():  # 分块写入文件
                    destination.write(chunk)
                destination.close()

                message = 2

                new_data = models.CenterData.objects.create(date=iddate, trend=trend, judge=judge, valueone=valueone,
                                                            valuetwo=valuetwo, filepath=filename)
                new_data.save()
                CenterData_form = CenterForm(locals())
                return render(request, 'centerdatamodify.html', locals())

    #差一个填入
    iddate = request.GET.get('datamodify')
    centerdata = models.CenterData.objects.get(date=iddate)
    trend = centerdata.trend
    judge = centerdata.judge
    valueone = centerdata.valueone
    valuetwo =centerdata.valuetwo
    CenterData_form = CenterForm(locals())
    return render(request, 'centerdatamodify.html', locals())


def center(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/superindex/")

    model = request.session['model']
    if model != 1001:
        return redirect("/superlogout/")

    kind = 1
    if request.method == "POST":
        CenterData_form = CenterForm(request.POST)
        message = 0

        if CenterData_form.is_valid():

            myFile = request.FILES.get("myfile", None)
            if not myFile:
                message = -1
                return render(request, 'CenterData.html', locals())

            if not myFile.name.endswith(".html"):
                message = -1
                return render(request, 'CenterData.html', locals())

            iddate = request.POST["inputdate"]
            trend = CenterData_form.cleaned_data['trend']
            judge = CenterData_form.cleaned_data['judge']
            valueone = CenterData_form.cleaned_data['valueone']
            valuetwo = CenterData_form.cleaned_data['valuetwo']
            try:
                centerdata = models.CenterData.objects.get(date=iddate)
                message = 1
                return render(request, 'CenterData.html', locals())
            except:
                message = 2

                filename = iddate + ".html"
                destination = open(os.path.join("C:\\centerdata",filename), 'wb+')  # 打开特定的文件进行二进制的写操作
                for chunk in myFile.chunks():  # 分块写入文件
                    destination.write(chunk)
                destination.close()

                new_data = models.CenterData.objects.create(date=iddate, trend=trend,judge=judge,valueone=valueone,
                    valuetwo=valuetwo,filepath=filename)
                new_data.save()
                CenterData_form = CenterForm()
                return render(request, 'CenterData.html', locals())

    CenterData_form = CenterForm()
    return render(request, 'CenterData.html', locals())

def superindex(request):
   kind = 1
   if not request.session.get('is_login', None):
       return redirect("/superlogin/")

   return render(request, 'sindex.html',locals())

def articleadd(request):
   if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
     return redirect("/superindex/")

   model = request.session['model']
   if model != 1001:
       return redirect("/superlogout/")

   kind = 1
   articlekind = 0
   if request.method == "POST":
       article_form = ArticleForm(request.POST)
       message = 2
       if article_form.is_valid():
           articletitle = article_form.cleaned_data['articletitle']
           articlecontent = article_form.cleaned_data['articlecontent']
           right = article_form.cleaned_data['right']
           articlecosttype = article_form.cleaned_data['articlecosttype']
           articlecost= article_form.cleaned_data['articlecost']
           downloadcosttype = article_form.cleaned_data['downloadcosttype']
           cost = article_form.cleaned_data['cost']
           cancommit = article_form.cleaned_data['cancommit']
           tag = article_form.cleaned_data['tag']
           articletag = article_form.cleaned_data['articletag']
           top= 0
           top = article_form.cleaned_data['top']
           authorize = 0
           authorize = article_form.cleaned_data['authorize']

           if tag == 0:
               if len(articletag) != 0:
                 try:
                    models.BlogTag.objects.get(name=articletag)
                 except:
                     new_tag = models.BlogTag.objects.create(name=articletag)
                     new_tag.save()
               else:
                   articletag = "其他"
           else:
               try:
                   taglist = models.BlogTag.objects.filter()
                   size = taglist.count()
                   if int(tag) > size:
                       articletag = "其他"
                   else:
                       articletag = taglist[int(tag) - 1].name
               except:
                   articletag = "其他"

           rightname = ""
           if right == "0":
               rightname = "游客"
           if right == "1":
               rightname = "普通会员"
           elif right == "2":
               rightname = "超级会员"
           elif right == "3":
               rightname = "白金会员"
           elif right == "4":
               rightname = "钻石会员"

           try:
               article = models.BlogArticle.objects.get(title=articletitle)
               message = 0
               article_form = ArticleForm(locals())
               return render(request, 'articleadd.html', locals())
           except:
               filepath = ""
               myFile = request.FILES.get("myfile", None)
               if myFile:
                   filepath = myFile.name
                   savepath = "C:\\articlefile\\" + articletitle
                   print(filepath)
                   if not os.path.exists(savepath):
                       os.makedirs(savepath)
                   destination = open(os.path.join(savepath, filepath), 'wb+')  # 打开特定的文件进行二进制的写操作

                   for chunk in myFile.chunks():  # 分块写入文件
                       destination.write(chunk)
                   destination.close()

               userid = request.session['user_id']
               message = 1
               new_article = models.BlogArticle.objects.create(title=articletitle, content=articlecontent,userid=userid,
                                                               filepath=filepath,cost=cost,user_right=right,rightname=rightname,
                                                               articlecosttype=articlecosttype,articlecost=articlecost,
                                                               filecosttype=downloadcosttype,cancommit=cancommit,tag=articletag,top=top
                                                               ,authorize=authorize)
               new_article.save()
               article_form = ArticleForm({"cost":0,"right":1,"articlecosttype":2,"articlecost":0,"downloadcosttype":2,"cancommit":0,"tag":1,"top":0,"authorize":0})
               return render(request, 'articleadd.html', locals())

   article_form = ArticleForm({"cost":0,"right":1,"articlecosttype":2,"articlecost":0,"downloadcosttype":2,"cancommit":0,"tag":1,"top":0,"authorize":0})
   return render(request, 'articleadd.html',locals())

def articlemodify(request):
   if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
     return redirect("/superindex/")

   model = request.session['model']
   if model != 1001:
       return redirect("/superlogout/")

   kind = 1
   articlekind = 1
   if request.method == "POST":
       article_form = ArticleForm(request.POST)
       message = 2
       if article_form.is_valid():
           articletitle = article_form.cleaned_data['articletitle']
           articlecontent = article_form.cleaned_data['articlecontent']
           right = article_form.cleaned_data['right']
           articlecosttype = article_form.cleaned_data['articlecosttype']
           articlecost = article_form.cleaned_data['articlecost']
           downloadcosttype = article_form.cleaned_data['downloadcosttype']
           cost = article_form.cleaned_data['cost']
           cancommit = article_form.cleaned_data['cancommit']
           tag = article_form.cleaned_data['tag']
           articletag = article_form.cleaned_data['articletag']
           top = 0
           top = article_form.cleaned_data['top']
           authorize = 0
           authorize = article_form.cleaned_data['authorize']
           if tag == 0:
               if len(articletag) != 0:
                   try:
                       models.BlogTag.objects.get(name=articletag)
                   except:
                       new_tag = models.BlogTag.objects.create(name=articletag)
                       new_tag.save()
               else:
                   articletag = "其他"
           else:
               try:
                   taglist = models.BlogTag.objects.filter()
                   size = taglist.count()
                   if int(tag) > size:
                       articletag = "其他"
                   else:
                       articletag = taglist[int(tag) - 1].name
               except:
                   articletag = "其他"

           rightname = ""
           if right == "0":
               rightname = "游客"
           if right == "1":
               rightname = "普通会员"
           elif right == "2":
               rightname = "超级会员"
           elif right == "3":
               rightname = "白金会员"
           elif right == "4":
               rightname = "钻石会员"

           filepath = ""
           myFile = request.FILES.get("myfile", None)
           if myFile:
               filepath = myFile.name

           userid = request.session['user_id']
           try:
               article = models.BlogArticle.objects.get(title=articletitle)
               article.content = articlecontent
               article.cost = cost
               article.user_right = right
               article.rightname = rightname
               article.articlecosttype = articlecosttype
               article.articlecost = articlecost
               article.filecosttype = downloadcosttype
               article.cancommit = cancommit
               article.tag = articletag
               article.top = top
               article.authorize = authorize
               if len(filepath) > 0:
                   savepath = "C:\\articlefile\\" + articletitle
                   article.filepath = filepath
                   if not os.path.exists(savepath):
                       os.makedirs(savepath)
                   else:
                       orginfilepath = article.filepath  # 获取原来路径删除文件
                       wholeorginfilepath = os.path.join(savepath, orginfilepath)
                       os.remove(wholeorginfilepath)

                   destination = open(os.path.join(savepath, filepath), 'wb+')  # 打开特定的文件进行二进制的写操作

                   for chunk in myFile.chunks():  # 分块写入文件
                       destination.write(chunk)
                   destination.close()

               article.save()
               message = 1
               article_form = ArticleForm(locals())
               return render(request, 'articleadd.html', locals())
           except:
               message = 0

               if len(filepath) > 0:
                   savepath = "C:\\articlefile\\" + articletitle

                   if not os.path.exists(savepath):
                       os.makedirs(savepath)
                   destination = open(os.path.join(savepath, filepath), 'wb+')  # 打开特定的文件进行二进制的写操作

                   for chunk in myFile.chunks():  # 分块写入文件
                       destination.write(chunk)
                   destination.close()

               new_article = models.BlogArticle.objects.create(title=articletitle, content=articlecontent,
                                                               userid=userid,
                                                               filepath=filepath, cost=cost, user_right=right,
                                                               rightname=rightname,
                                                               articlecosttype=articlecosttype, articlecost=articlecost,
                                                               filecosttype=downloadcosttype, cancommit=cancommit,tag=articletag)
               new_article.save()
               article_form = ArticleForm({"cost":0,"right":1,"articlecosttype":2,"articlecost":0,"downloadcosttype":2,"cancommit":1,"tag":1})
               return render(request, 'articleadd.html', locals())

   articletitle = request.GET.get('articletitle')
   article = models.BlogArticle.objects.get(title=articletitle)
   articlecontent = article.content
   cost = article.cost
   right = article.user_right
   articlecosttype = article.articlecosttype
   articlecost = article.articlecost
   downloadcosttype = article.filecosttype
   cancommit = article.cancommit
   articletag = article.tag
   top = article.top
   authorize = article.authorize
   tag = 1
   try:
       tagget = models.BlogTag.objects.get(name=articletag)
       tag = int(tagget.id)
   except:
       try:
          taglist = models.BlogTag.objects.filter()
          size = taglist.count()
          tag = size + 1
       except:
           tag = 0

   article_form = ArticleForm(locals())
   return render(request, 'articleadd.html',locals())

def superlogin(request):
    kind = 1

    if request.session.get('is_login', None):
        model = request.session['model']
        if model != 1001:
            return redirect('/superlogout/')

    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.Superuser.objects.get(userid=username)
                if user.password == password:
                    request.session['is_login'] = True
                    request.session['user_id'] = user.userid
                    request.session['user_name'] = user.userid
                    request.session['model'] = 1001
                    return redirect('/superindex/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'login.html', locals())
    login_form = UserForm()
    return render(request, 'login.html', locals())

def superlogout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/superlogin/")
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/superlogin/")

def articlemanage(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/superindex/")

    model = request.session['model']
    if model != 1001:
        return redirect("/superlogout/")

    kind = 1
    managemodel = 0

    article_list = models.BlogArticle.objects.filter(delete_flag=0)


    print(article_list)

    paginator = Paginator(article_list, 15)
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

    return render(request, 'articlemanage.html',locals())

def articledelete(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/superindex/")

    model = request.session['model']
    if model != 1001:
        return redirect("/superlogout/")

    kind = 1
    articletitle = request.GET.get('articletitle')
    article = models.BlogArticle.objects.get(title=articletitle)
    article.delete_flag = 1
    article.save()

    return redirect("/articlemanage/")

def articlerecoverlist(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/superindex/")

    model = request.session['model']
    if model != 1001:
        return redirect("/superlogout/")

    managemodel = 1
    kind = 1
    article_list = models.BlogArticle.objects.filter(delete_flag=1)
    paginator = Paginator(article_list, 15)
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

    return render(request, 'articlemanage.html',locals())

def articlerecover(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/superindex/")

    model = request.session['model']
    if model != 1001:
        return redirect("/superlogout/")

    kind = 1
    articletitle = request.GET.get('articletitle')
    article = models.BlogArticle.objects.get(title=articletitle)
    article.delete_flag = 0
    article.save()

    return redirect("/articlerecoverlist/")

def articlecommit(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/superindex/")

    model = request.session['model']
    if model != 1001:
        return redirect("/superlogout/")

    titlename = request.GET.get("articletitle")
    kind = 1

    try:
        commit_list = models.ArticleContain.objects.filter(title=titlename,commentflag=1).order_by('-firstreaddate')
        already_list = models.ArticleContain.objects.filter(title=titlename,commentflag=2).order_by('-firstreaddate')
        try:
            if already_list:
                commit_list.extend(already_list)
        except:
            commit_list = already_list

        paginator = Paginator(commit_list, 15)
        # 从前端获取当前的页码数,默认为1
        page = request.GET.get('page', 1)


        # 把当前的页码数转换成整数类型
        currentPage = int(page)

        try:
            commit_list = paginator.page(page)  # 获取当前页码的记录
        except PageNotAnInteger:
            commit_list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
        except EmptyPage:
            commit_list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容

        return render(request, 'articlecommitmanage.html', locals())
    except:
        return redirect("/superindex/")

def commitmanage(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/superindex/")

    model = request.session['model']
    if model != 1001:
        return redirect("/superlogout/")

    titlename = request.GET.get("articletitle")
    userid = request.GET.get("userid")
    manage = request.GET.get("manage")
    kind = 1

    articlecontain = models.ArticleContain.objects.get(userid=userid,title=titlename)

    if articlecontain:
        if int(manage) == 0:
            articlecontain.comment = ""
            articlecontain.commentflag = 0
            articlecontain.save()
        elif int(manage) == 2:
            articlecontain.commentflag = 2
            articlecontain.save()
        elif int(manage) == 3:
            articlecontain.comment = ""
            articlecontain.commentflag = 3
            articlecontain.save()

    try:
        commit_list = models.ArticleContain.objects.filter(title=titlename,commentflag=1).order_by('-firstreaddate')
        already_list = models.ArticleContain.objects.filter(title=titlename,commentflag=2).order_by('-firstreaddate')
        try:
            commit_list.extend(already_list)
        except:
            commit_list = already_list

        paginator = Paginator(commit_list, 15)
        # 从前端获取当前的页码数,默认为1
        page = request.GET.get('page', 1)


        # 把当前的页码数转换成整数类型
        currentPage = int(page)

        try:
            commit_list = paginator.page(page)  # 获取当前页码的记录
        except PageNotAnInteger:
            commit_list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
        except EmptyPage:
            commit_list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容

        return render(request, 'articlecommitmanage.html', locals())
    except:
        return redirect("/superindex/")


def activecode(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/superindex/")

    model = request.session['model']
    if model != 1001:
        return redirect("/superlogout/")

    userid = request.session["user_id"]
    if request.method == "POST":
        info = "生成激活码失败，请重试！"
        try:
            precent = request.POST["precent"]
            code = get_active_code()
            if len(code) == 0:
                return render(request, 'commoninfotran.html', {"info": info})

            newcode = models.SpreadCode.objects.create(codeid=code, getuser=userid, spreadprecent=precent)
            newcode.save()
            return redirect("/activecode/")
        except:
            return render(request, 'commoninfotran.html', {"info": info})


    kind = 1
    code_list = []
    code_form = ActiveCodeform()

    try:
        code_list = models.SpreadCode.objects.all().order_by('-gettime')
    except:
        code_list = []

    paginator = Paginator(code_list, 15)
    # 从前端获取当前的页码数,默认为1
    page = request.GET.get('page', 1)

    # if int(page) > article_list.count()/10:
    # raise Http404("Page does not exist")
    # 把当前的页码数转换成整数类型
    currentPage = int(page)

    try:
        code_list = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        code_list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        code_list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容

    return render(request, 'activecodemanage.html',locals())

@loginverify
def cashmanage(request):
    kind = 1
    contentname = "提现审核"
    order_list = []

    try:
        order_list = models.CashOrder.objects.filter(iswechat=0,orderstate=2).order_by('time')
    except:
        info="系统读取数据不成功，请检查数据库连接，或稍后再试！"
        return render(request, 'commoninfotran.html')

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

    return render(request, 'cashmanage.html',locals())

@loginverify
def cashapprove(request):
    orderid = request.GET.get('id')
    identify = int(request.GET.get('identify'))
    page = request.GET.get('page', 1)

    try:
        if identify == 1:
            order = models.CashOrder.objects.get(orderid=orderid)
            order.orderstate = 3
            order.save()
        else:
            order = models.CashOrder.objects.get(orderid=orderid)
            userid = order.userid
            meony = order.meony
            order.orderstate = -1
            order.appeal = 0
            order.save()
            # 失败返回钱数
            User = models.Commonuser.objects.get(userid=userid)
            User.spreadmeony = F('spreadmeony') + meony
            User.save()
            # 恢复次数
            BindUser = models.CashBind.objects.get(userid=userid)
            BindUser.banktimes = BindUser.banktimes + 1
            BindUser.save()
    except:
        info = "系统写入参数不成功，请检查数据库连接，或稍后再试！"
        return render(request, 'commoninfotran.html')

    url = "/cashmanage/?page=" + str(page)
    return redirect(url)

@loginverify
def cashbank(request):
    kind = 1
    contentname = "提现打款"
    order_list = []

    try:
        order_list = models.CashOrder.objects.filter(iswechat=0,orderstate=3).order_by('time')
    except:
        info="系统读取数据不成功，请检查数据库连接，或稍后再试！"
        return render(request, 'commoninfotran.html')

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

    return render(request, 'cashtobank.html',locals())

@loginverify
def cashsucess(request):
    orderid = request.GET.get('id')
    identify = int(request.GET.get('identify'))
    page = request.GET.get('page', 1)

    try:
        if identify == 1:
            order = models.CashOrder.objects.get(orderid=orderid)
            order.orderstate = 1
            order.appeal = 0
            order.save()
        else:
            order = models.CashOrder.objects.get(orderid=orderid)
            userid = order.userid
            meony = order.meony
            order.orderstate = 0
            order.appeal = 0
            order.save()
            #失败返回钱数
            User = models.Commonuser.objects.get(userid=userid)
            User.spreadmeony = F('spreadmeony') + meony
            User.save()
            #恢复次数
            BindUser =  models.CashBind.objects.get(userid=userid)
            BindUser.banktimes = BindUser.banktimes + 1
            BindUser.save()
    except:
        info = "系统写入参数不成功，请检查数据库连接，或稍后再试！"
        return render(request, 'commoninfotran.html')

    url = "/cashbank/?page=" + str(page)
    return redirect(url)

@loginverify
def cashlist(request):
    kind = 1
    contentname = "所有提现订单"
    order_list = []

    try:
        order_list = models.CashOrder.objects.all().order_by('-time')
    except:
        info="系统读取数据不成功，请检查数据库连接，或稍后再试！"
        return render(request, 'commoninfotran.html')

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

    return render(request, 'cashorderlist.html',locals())

@loginverify
def cashappealmanage(request):
    kind = 1
    order_list = []

    try:
        order_list = models.CashOrder.objects.filter(appeal=1).order_by('time')
    except:
        info="系统读取数据不成功，请检查数据库连接，或稍后再试！"
        return render(request, 'commoninfotran.html')

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

    return render(request, 'cashappeallist.html',locals())

@loginverify
def cashappeal(request):
    orderid = request.GET.get('id')
    page = request.GET.get('page', 1)

    try:
        order = models.CashOrder.objects.get(orderid=orderid)
        order.appeal = 2
        order.save()

    except:
        info = "系统写入参数不成功，请检查数据库连接，或稍后再试！"
        return render(request, 'commoninfotran.html')

    url = "/managecashlist/?page=" + str(page)
    return redirect(url)