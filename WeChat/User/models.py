# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from DjangoUeditor.models import UEditorField


class CenterData(models.Model):
    date = models.CharField(db_column='iddate',primary_key=True,max_length=16)  # Field name made lowercase.
    trend = models.IntegerField(db_column='trend', default=0)
    judge = models.TextField(db_column='judge', default='')
    valueone = models.IntegerField(db_column='valueone', default=0)
    valuetwo = models.IntegerField(db_column='valuetwo', default=0)
    filepath = models.CharField(db_column='filepath', max_length=256)

    class Meta:
        managed = True
        db_table = 'centerdata'

class BlogTag(models.Model):
    name = models.CharField(db_column='tag', max_length=20)

    class Meta:
        managed = True
        db_table = 'blogtag'

class BlogArticle(models.Model):
    userid = models.CharField(db_column='UserID',max_length=16)  # Field name made lowercase.
    title = models.CharField(db_column='title', max_length=100)
    content = UEditorField(db_column='content', default='')
    create_time = models.DateTimeField(db_column='createtime', auto_now = True)
    modify_time = models.DateTimeField(db_column='modifytime',auto_now = True)
    click_nums = models.IntegerField(db_column='clickrate', default=0)
    tag = models.CharField(db_column='tag', max_length=20,default='其他')
    delete_flag = models.IntegerField(db_column='deleteflag', default=0)
    filecosttype = models.IntegerField(db_column='filecosttype', default=0)#0:免费；1、积分；2、缝芽币
    cost = models.IntegerField(db_column='cost', default=0)
    user_right = models.IntegerField(db_column='right', default=1)
    filepath = models.CharField(db_column='filepath', max_length=256,default="")
    rightname = models.CharField(db_column='rightname', max_length=16,default='普通会员')
    articlecosttype = models.IntegerField(db_column='articlecosttype', default=0)#0:免费；1、积分；2、缝芽币
    articlecost = models.IntegerField(db_column='articlecost', default=0)
    score = models.IntegerField(db_column='score', default=50)#为方便且节省资源，防止出错，所有涉及到小数的全部以整数代替，/10.0为真实的数值
    scorernumber = models.IntegerField(db_column='scorernumber', default=0)#评分人数
    class Meta:
        managed = True
        db_table = 'blogarticle'

class Accoountgiveout(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    accountid = models.CharField(db_column='AccountID', max_length=128)  # Field name made lowercase.
    value = models.IntegerField(db_column='Value')  # Field name made lowercase.
    date = models.DateTimeField(db_column='Date')  # Field name made lowercase.
    balance = models.IntegerField(db_column='Balance', blank=True, null=True)  # Field name made lowercase.
    totalsum = models.IntegerField(db_column='TotalSum', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'accoountgiveout'


class Accountuser(models.Model):
    userid = models.CharField(db_column='UserID', primary_key=True, max_length=128)  # Field name made lowercase.
    password = models.CharField(db_column='PassWord', max_length=48, blank=True)  # Field name made lowercase.
    precent = models.IntegerField(db_column='Precent', blank=True)  # Field name made lowercase.
    commonusercount = models.IntegerField(db_column='CommonUserCount', blank=True, null=True)  # Field name made lowercase.
    lastnum = models.IntegerField(db_column='LastNum', blank=True, null=True)  # Field name made lowercase.
    balance = models.IntegerField(db_column='Balance', blank=True, null=True)  # Field name made lowercase.
    totalsum = models.IntegerField(db_column='TotalSum', blank=True, null=True)  # Field name made lowercase.
    identy = models.CharField(db_column='Identy', max_length=24, blank=True, null=True)  # Field name made lowercase.
    cardid = models.CharField(db_column='CardID', max_length=24, blank=True, null=True)  # Field name made lowercase.
    headpath = models.CharField(db_column='HeadPath', max_length=256, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'accountuser'


class Acount(models.Model):
    acountname = models.CharField(db_column='AcountName', primary_key=True, max_length=128)  # Field name made lowercase.
    acountuser = models.CharField(db_column='AcountUser', max_length=128, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'acount'

class Commonuser(models.Model):
    userid = models.CharField(db_column='UserID', primary_key=True, max_length=128)  # Field name made lowercase.
    password = models.CharField(db_column='PassWord', max_length=48)  # Field name made lowercase.
    acountuser = models.CharField(db_column='AcountUser', max_length=128)  # Field name made lowercase.
    source = models.CharField(db_column='Source', max_length=128)  # Field name made lowercase.
    cardid = models.CharField(db_column='CardID', max_length=24, blank=True, null=True)  # Field name made lowercase.
    identify = models.CharField(db_column='Identify', max_length=24, blank=True, null=True)  # Field name made lowercase.
    level = models.IntegerField(db_column='Level')  # Field name made lowercase.
    headpath = models.CharField(db_column='HeadPath', max_length=256, blank=True, null=True)  # Field name made lowercase.
    memberdate = models.DateTimeField(db_column='MemberDate', blank=True, null=True)  # Field name made lowercase.
    recharge = models.IntegerField(db_column='Recharge', blank=True, null=True)  # Field name made lowercase.
    currentrechargedate = models.DateTimeField(db_column='CurrentRechargeDate', blank=True, null=True)  # Field name made lowercase.
    currentrecharge = models.IntegerField(db_column='CurrentRecharge', blank=True, null=True)  # Field name made lowercase.
    registerdate = models.DateTimeField(db_column='RegisterDate',auto_now = True)  # Field name made lowercase.
    firstlogindate = models.DateTimeField(db_column='FirstLoginDate', blank=True, null=True)  # Field name made lowercase.
    currnetlogindate = models.DateTimeField(db_column='CurrnetLoginDate', blank=True, null=True)  # Field name made lowercase.
    isfree = models.IntegerField(db_column='IsFree', blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=32, blank=True, null=True)  # Field name made lowercase.
    phonenum = models.CharField(db_column='PhoneNum', max_length=16, blank=True, null=True)
    fengyacoin = models.IntegerField(db_column='FengYaCoin', blank=True,default=0)
    class Meta:
        managed = True
        db_table = 'commonuser'

class Fileright(models.Model):
    userid = models.CharField(db_column='UserID', max_length=128)
    title = models.CharField(db_column='title', max_length=100)
    buydate = models.DateTimeField(db_column='BuyDate',auto_now = True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'fileright'

class Companymoney(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    userid = models.CharField(db_column='UserID', max_length=128)  # Field name made lowercase.
    usergroup = models.CharField(db_column='UserGroup', max_length=24)  # Field name made lowercase.
    date = models.DateTimeField(db_column='Date')  # Field name made lowercase.
    type = models.IntegerField(db_column='Type')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'companymoney'


class Everydaycomment(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    date = models.DateTimeField(db_column='Date')  # Field name made lowercase.
    content = models.CharField(db_column='Content', max_length=512, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'everydaycomment'


class Oprate(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    user = models.CharField(db_column='User', max_length=128)  # Field name made lowercase.
    oprate = models.CharField(db_column='Oprate', max_length=256)  # Field name made lowercase.
    date = models.DateTimeField(db_column='Date')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'oprate'


class Set(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    setvalue = models.CharField(db_column='SetValue', max_length=24)  # Field name made lowercase.
    charge = models.IntegerField(db_column='Charge')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'set'

class Topuser(models.Model):
    userid = models.CharField(db_column='UserID', primary_key=True, max_length=16)  # Field name made lowercase.
    password = models.CharField(db_column='PassWord', max_length=16)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'topuser'

class Superuser(models.Model):
    userid = models.CharField(db_column='UserID', primary_key=True, max_length=16)  # Field name made lowercase.
    password = models.CharField(db_column='PassWord', max_length=16)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'superuser'

class Usercharge(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    userid = models.IntegerField(db_column='UserID')  # Field name made lowercase.
    account = models.CharField(db_column='Account', max_length=128)  # Field name made lowercase.
    source = models.CharField(db_column='Source', max_length=128)  # Field name made lowercase.
    charge = models.IntegerField(db_column='Charge')  # Field name made lowercase.
    chargedate = models.DateTimeField(db_column='ChargeDate')  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=16, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'usercharge'

#教程用户评论及收藏评分等
class ArticleContain(models.Model):
    userid = models.CharField(db_column='UserID', max_length=128)
    title = models.CharField(db_column='title', max_length=100)
    firstreaddate = models.DateTimeField(db_column='ReadDate',auto_now = True)  # Field name made lowercase.
    score = models.IntegerField(db_column='score', default=0)#评分，0默认为未评分
    comment = models.CharField(db_column='comment', max_length=500,default='')  # Field name made lowercase.
    collect = models.IntegerField(db_column='collect', default=0)#是否收藏

    class Meta:
        managed = True
        db_table = 'articlecontain'