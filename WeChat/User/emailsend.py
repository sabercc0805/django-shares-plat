from random import Random  # 用于生成随机码
from django.core.mail import send_mail  # 发送邮件模块
from django.conf import settings    # setting.py添加的的配置信息
from User import models
from datetime import datetime
from django.utils import timezone

def random_str(randomlength=6):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str

def send_code_email(email,strcode,send_type="register"):
    # 初始化为空
    email_title = ""
    email_body = ""
    # 如果为注册类型
    if send_type == "register":
        email_title = "逢芽网——注册激活"
        # email_body = "请点击下面的链接激活你的账号:http://127.0.0.1:8000/active/{0}".format(code)
        email_body = "您的邮箱注册激活码为：{0}, 该激活码有效时间为5分钟，请及时进行验证。\n广西缝芽信息科技有限公司祝您生活愉快，股市飘红！".format(strcode)
        # 发送邮件
        send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
        if not send_status:
            return False
    if send_type == "cash":
        email_title = "逢芽网——提现申请"
        email_body = "您的提现验证码为：{0}, 该验证码有效时间为5分钟，请及时进行验证。\n广西缝芽信息科技有限公司祝您生活愉快！".format(strcode)
        # 发送邮件
        send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
        if not send_status:
            return False
    if send_type == "bindbank":
        email_title = "逢芽网——绑定银行卡"
        email_body = "您的绑定验证码为：{0}, 该验证码有效时间为5分钟，请及时进行验证。\n广西缝芽信息科技有限公司祝您生活愉快！".format(strcode)
        # 发送邮件
        send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
        if not send_status:
            return False
    return True

def judege_spread_level(totalmeony):
    level = 1

    judge = int(totalmeony)/100

    if judge < 50:
        level = 1
    elif judge < 100:
        level = 2
    elif judge < 500:
        level = 3
    elif judge < 1000:
        level = 4
    elif judge < 2000:
        level = 5
    elif judge < 5000:
        level = 6
    elif judge < 10000:
        level = 7
    elif judge < 20000:
        level = 8
    elif judge < 50000:
        level = 9
    else:
        level = 10

    return level


def judege_spread_precent(level):
    spreadprecent = 5

    nlevel = int(level)

    if nlevel == 1:
        spreadprecent = 5
    elif nlevel == 2:
        spreadprecent = 6
    elif nlevel == 3:
        spreadprecent = 7
    elif nlevel == 4:
        spreadprecent = 9
    elif nlevel == 5:
        spreadprecent = 11
    elif nlevel == 6:
        spreadprecent = 13
    elif nlevel == 7:
        spreadprecent = 16
    elif nlevel == 8:
        spreadprecent = 20
    elif nlevel == 9:
        spreadprecent = 24
    elif nlevel == 10:
        spreadprecent = 30

    return spreadprecent

def get_user_pravite_key():
    key = ""
    bContinue = True
    while bContinue:
        key = random_str(8)
        user_list = []
        try:
            user_list = models.Commonuser.objects.filter(spreadcode=key)
            if user_list.count() == 0:
                bContinue = False
        except:
             bContinue = False

    return key

def get_active_spread_precent(activecode,activeuser):
    spreadprecent = 5
    try:
        codeobject = models.SpreadCode.objects.get(codeid=activecode)

        if codeobject.isused == 1:
            spreadprecent = 1#已使用
            return spreadprecent

        spreadprecent = codeobject.spreadprecent
        codeobject.userid = activeuser
        codeobject.isused = 1
        date = datetime.now()
        detester = date.strftime('%Y-%m-%d')
        codeobject.usetime = detester
        codeobject.save()

    except:
        spreadprecent = 0 #不存在
    return  spreadprecent

def next_spread_level_value(level):
    value = 50

    nlevel = int(level)

    if nlevel == 1:
        value = 50
    elif nlevel == 2:
        value = 100
    elif nlevel == 3:
        value = 500
    elif nlevel == 4:
        value = 1000
    elif nlevel == 5:
        value = 2000
    elif nlevel == 6:
        value = 5000
    elif nlevel == 7:
        value = 10000
    elif nlevel == 8:
        value = 20000
    elif nlevel == 9:
        value = 50000
    elif nlevel == 10:
        value = 50000

    return value

def get_active_code():
    key = ""
    bContinue = True
    while bContinue:
        key = random_str(10)
        code_list = []
        try:
            code_list = models.SpreadCode.objects.filter(codeid=key)
            if code_list.count() == 0:
                bContinue = False
        except:
             bContinue = False

    return key

def verifycode(code,type,email):
    result = 0

    try:
        findcode = models.CashCode.objects.get(email=email)
        if findcode.codeid == code and findcode.type == type:
            getdate = findcode.gettime
            strdate = getdate.strftime("%Y-%m-%d %H:%M:%S")
            beforedate = datetime.strptime(strdate, '%Y-%m-%d %H:%M:%S')
            nowdate = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
            trandate = datetime.strptime(nowdate, '%Y-%m-%d %H:%M:%S')

            delta = trandate - beforedate
            interval = delta.seconds
            if interval / 60 > 5:
                result = -1
                return result

            findcode.delete()
            result = 1
            return result
        else:
            result = 0
            return result
    except:
        result = 0
        return  result

    return result

def ScreenAppid(userid):#筛选用户关注的公众号
    result = 0
    appid = ""
    app_list = []
    concern_list = []
    list_new = []
    try:
        app_list = models.AuthorizeInfo.objects.filter(type=1).values_list('appid',flat=True)
        concern_list = models.ConcernInfo.objects.filter(userid=userid).values_list('appid',flat=True)
        list_new = list(set(app_list).difference(set(concern_list)))
        count = len(list_new)
        if count > 0:
            random = Random()
            appid = list_new[random.randint(0, count-1)]
            print("src1")
            print(appid)
            result = 0
        else:
            result = 2#已无可关注的公众号

        return result, appid
    except:
        result = -1
        return result,appid

