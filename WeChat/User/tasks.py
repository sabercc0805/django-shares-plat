from __future__ import absolute_import,unicode_literals
from celery import task
from User import models
from django.utils import timezone
from datetime import datetime
from django.db.models import F
import logging

from User.email import judege_spread_precent
from User.email import judege_spread_level

logger = logging.getLogger(__name__)

@task
def spread_entry():
    nowdate = timezone.now().date()
    checkdate = nowdate - datetime.timedelta(days=8)

    try:
        order_list=[]
        order_list = models.OrderOver.objects.filter(orderstate=1,spreadentry=0,chargedate__lte=checkdate)

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

            if BindUser.spreadprecent != spreadprecnet:
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