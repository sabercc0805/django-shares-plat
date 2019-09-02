"""WeChat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
]

from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from User import home
from User import wechatpay
from superuser import super
from account import account

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',home.index),
    url(r'^index/', home.index),
    url(r'^login/', home.login),
    url(r'^register/', home.register),
    url(r'^logout/', home.logout),
    url(r'^superlogin/', super.superlogin),
    url(r'^superlogout/', super.superlogout),
    url(r'^superindex/', super.superindex),
    url(r'^accountlogin/', account.accountlogin),
    url(r'^accountlogout/', account.accountlogout),
    url(r'^captcha', include('captcha.urls')),
    url(r'^userinfo/', home.userinfo),
    url(r'^article/', home.article),
    url(r'^articlecontent/', home.articlecontent),
    url(r'^download/', home.download),
    url(r'^changepassword/', home.changepassword),
    url(r'^articleadd/', super.articleadd),
    url(r'^articlemodify/', super.articlemodify),
    url(r'^articledelete/', super.articledelete),
    url(r'^articlerecoverlist/', super.articlerecoverlist),
    url(r'^articlerecover/', super.articlerecover),
    url(r'^articlemanage/', super.articlemanage),
    url(r'^center/', super.center),
    url(r'^datamanage/', super.centerdatamanage),
    url(r'^datadelete/', super.centerdatadelete),
    url(r'^datamodify/', super.centerdatamodify),
    url(r'^showdata/', super.showdata),
    url(r'^iframe/', super.iframe),
    url(r'^showcommondata/', home.showdata),
    url(r'^iframecommon/', home.iframe),
    url(r'^about/', home.about),
    url(r'^ad/', home.advertisement),
    url(r'^ueditor/', include('DjangoUeditor.urls')),
    url(r'^finger/', home.ajax_finger),
    url(r'^collect/', home.ajax_collect),
    url(r'^commit/', home.ajax_commit),
    url(r'^commitlist/', super.articlecommit),
    url(r'^commitmanage/', super.commitmanage),
    url(r'^ceshi/', home.ceshi),
    url(r'^userarticleoperate/', home.userarticleoperate),
    url(r'^usercancel/', home.usercancel),
    url(r'^sign/', home.ajax_sign),
    url(r'^wxpay/', wechatpay.wxpay),
    url(r'^credit/', home.credits),
    url(r'^coin/', home.coin),
    url(r'^exchange/', home.exchange),
    url(r'^checkorder/', home.checkorder),
    url(r'^chargeresult/', home.chargeresult),
    url(r'^orderlist/', home.orderlist),
    url(r'^apeal/', home.ajax_apeal),
    url(r'^getcode/', home.ajax_getcode),
    url(r'^checkresult/', wechatpay.check_wxpay),
]

