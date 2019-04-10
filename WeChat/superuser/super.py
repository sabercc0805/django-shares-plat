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
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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

    filepath=os.path.join("..\\templates\\centerdata", keypath)
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
                destination = open(os.path.join("C:\\django-shares-plat\\WeChat\\templates\\centerdata",filename), 'wb+')  # 打开特定的文件进行二进制的写操作
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
           try:
               article = models.BlogArticle.objects.get(title=articletitle)
               message = 0
               article_form = ArticleForm(locals())
               return render(request, 'articleadd.html', locals())
           except:
               userid = request.session['user_id']
               message = 1
               new_article = models.BlogArticle.objects.create(title=articletitle, content=articlecontent,userid=userid)
               new_article.save()
               article_form = ArticleForm()
               return render(request, 'articleadd.html', locals())

   article_form = ArticleForm()
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
           try:
               article = models.BlogArticle.objects.get(title=articletitle)
               article.content = articlecontent
               article.save()
               message = 1
               article_form = ArticleForm(locals())
               return render(request, 'articleadd.html', locals())
           except:
               message = 0
               new_article = models.BlogArticle.objects.create(title=articletitle, content=articlecontent)
               new_article.save()
               article_form = ArticleForm()
               return render(request, 'articleadd.html', locals())

   articletitle = request.GET.get('articletitle')
   article = models.BlogArticle.objects.get(title=articletitle)
   articlecontent = article.content
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