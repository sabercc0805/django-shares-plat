# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


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
    registerdate = models.DateTimeField(db_column='RegisterDate')  # Field name made lowercase.
    firstlogindate = models.DateTimeField(db_column='FirstLoginDate', blank=True, null=True)  # Field name made lowercase.
    currnetlogindate = models.DateTimeField(db_column='CurrnetLoginDate', blank=True, null=True)  # Field name made lowercase.
    isfree = models.IntegerField(db_column='IsFree', blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=32, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'commonuser'


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
