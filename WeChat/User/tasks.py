from __future__ import absolute_import,unicode_literals
from celery import task
from User import models
from django.utils import timezone
from datetime import datetime
from datetime import timedelta
from django.db.models import F
from django.db.models import Q
import logging

from User.emailsend import judege_spread_precent
from User.emailsend import judege_spread_level
from User.wechatpay import excutewechatcash
from User.wechatpay import excuteresearch
from User.wechatpay import recoverdaytimes
from User.wechatpay import recovermonthtimes
from User.wechatpay import get_plattocken
from User.wechatpay import recoverappstate
logger = logging.getLogger(__name__)

@task
def spread_entry():
    nowdate = timezone.now().date()
    checkdate = nowdate - timedelta(days=1)
    
    try:
        order_list=[]
        order_list = models.OrderOver.objects.filter(~Q(binduser= ""),orderstate=1,spreadentry=0,chargedate__lte=checkdate)

        for order in order_list:
            md5 = order.binduser
            userid = order.userid
            dividemoney = order.dividemoney
            User = models.Commonuser.objects.get(userid=userid)
            User.bindmenoy = F('bindmenoy') + dividemoney
            User.save()
            BindUser = models.Commonuser.objects.get(md5=md5)                      
            totalmeony = BindUser.totalmeony
            totalmeony += dividemoney
            level = judege_spread_level(totalmeony)
            spreadprecnet = judege_spread_precent(level)
           
            if BindUser.isaccount != 1:
                BindUser.spreadprecent = spreadprecnet

            BindUser.totalmeony = F('totalmeony') + dividemoney
            BindUser.spreadmeony = F('spreadmeony') + dividemoney
            BindUser.save()
            order.spreadentry = 1
            order.save()
    except:
        strtime = nowdate.strftime('YYYY-MM-DD')
        strlog = str + " 今日同步推广用户入账数据失败，请重新同步！"
        logger.info(strlog)
        return

    strtime = nowdate.strftime('YYYY-MM-DD')
    strlog = str + " 今日同步推广用户入账数据成功！"
    logger.info(strlog)
    return

@task
def excutetaskcash():
    excutewechatcash()
    return

@task
def excutetaskresearch():
    excuteresearch()
    return

@task
def recovertaskdaytimes():
    recoverdaytimes()
    return

@task
def recovertaskmonthtimes():
    recovermonthtimes()
    return

@task
def get_task_plattocken():
    get_plattocken()
    return

@task
def recovertaskappstate():
    recoverappstate()
    return