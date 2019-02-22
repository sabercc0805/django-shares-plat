import os
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from User import models
from User.forms import UserForm
from User.forms import ArticleForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def superindex(request):
   kind = 1
   if not request.session.get('is_login', None):
       return redirect("/superlogin/")

   return render(request, 'superindex.html',locals())

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