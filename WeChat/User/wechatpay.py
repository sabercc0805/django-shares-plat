#微信支付   部分通用函数
import os
import qrcode
from random import Random
import time
from bs4 import BeautifulSoup
from django.utils import timezone
from django.http import FileResponse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.template import RequestContext
from User import models
from datetime import datetime
from django.forms.models import model_to_dict
from django.utils.http import urlquote
from django.http import JsonResponse
from .forms import Coinform
from django.db.models import F
from django.views.decorators.csrf import csrf_exempt

import requests
import socket
import random
import hashlib
import json
from User.WXBizMsgCrypt import WXBizMsgCrypt


_APP_ID = "wxb5d226f10420789f"
_MCH_ID = "1543525851"
_API_KEY = "zzhr1990hr0805zjw1991pmf04251111"

_UFDODER_URL = "https://api.mch.weixin.qq.com/pay/unifiedorder" #url是微信下单api
_NOTIFY_URL = "https://www.yuntaoz.cn/checkresult/"
_PAYMENT_URL = "https://api.mch.weixin.qq.com/mmpaymkttransfers/promotion/transfers"#企业支付url
_PAYMENTCHECK_URL = "https://api.mch.weixin.qq.com/mmpaymkttransfers/gettransferinfo"

#myname = socket.getfqdn(socket.gethostname())
_CREATE_IP = "127.0.0.1"#socket.gethostbyname(myname)  # 发起支付请求的ip

component_appid = "wxc0ad5e0f7a6d4e4f"
encodingAESKey = "zzhr19900805hr19910425zhx19631228zjwpmf1234"
component_tocken = "19900805"
component_secret = "d71a4c2cbc798ab4348c9369ff5caada"

usererror_dict = {"AMOUNT_LIMIT":"金额超限,您的提现金额超限，请提现在100元以上，2000元以下",
                    "OPENID_ERROR":"Openid错误，您是否取消关注石缝芽数据公众号，请关注后重新绑定",
                  "NOTENOUGH":"很抱歉，当前公众号提现金额受限，请您明日再试",
                  "NAME_MISMATCH":"您的微信号实名认证与本网站实名认证不符，请改绑提现微信后重试",
                  "MONEY_LIMIT":"很抱歉，今日公众号提现金额已达上限，请您明日再试",
                  "V2_ACCOUNT_SIMPLE_BAN": "您的微信号尚未实名认证无法提现，请实名后重试（提示：实名认证需与本网站一致）",
                  "SENDNUM_LIMIT":"很抱歉，您的微信提现次数今日已达上限，请您明日重试"}

syserror_dict = {"NO_AUTH":"没有该接口权限","PARAM_ERROR":"参数错误",
              "XML_ERROR": "Post内容出错","FATAL_ERROR":"两次请求参数不一致",
              "RECV_ACCOUNT_NOT_ALLOWED":"收款账户不在收款账户列表","PAY_CHANNEL_NOT_ALLOWED":"本商户号未配置API发起能力",
                 "SIGN_ERROR":"签名错误","CA_ERROR":"商户API证书校验出错","PARAM_IS_NOT_UTF8":"请求参数中包含非utf8编码字符",
                 }

retryerror_dict = {"SEND_FAILED":"付款错误","SYSTEMERROR":"系统繁忙，请稍后再试"}

# 定义字典转XML的函数
def trans_dict_to_xml(data_dict):
    data_xml = []
    for k in sorted(data_dict.keys()):  # 遍历字典排序后的key
        v = data_dict.get(k)  # 取出字典中key对应的value
        if k == 'detail' and not v.startswith('<![CDATA['):  # 添加XML标记
            v = '<![CDATA[{}]]>'.format(v)
        data_xml.append('<{key}>{value}</{key}>'.format(key=k, value=v))
    return '<xml>{}</xml>'.format(''.join(data_xml))  # 返回XML

# 定义XML转字典的函数
def trans_xml_to_dict(data_xml):
    soup = BeautifulSoup(data_xml, features='xml')
    xml = soup.find('xml')  # 解析XML
    if not xml:
        return {}
    data_dict = dict([(item.name, item.text) for item in xml.find_all()])
    return data_dict


# 发起微信支付
#orderstart发起支付即将订单写入
def wxpay(request):
    kind = 0

    if not request.session.get('is_login', None):
        return redirect('/index/')

    model = request.session['model']
    if model != 1000:
        return redirect("/logout/")

    if request.method == "POST":
        coin_form = Coinform(request.POST)
        chargetype = -1
        success = 0
        if coin_form.is_valid():
            chargetype = int(coin_form.cleaned_data['chargetype'])
        else:
            errortype = -2
            return render(request, 'chargetran.html', {"chargetype": errortype, "success": success})

        username = request.session['user_id']
        precent = 100
        coin = 0

        switch = {
            0: 10,
            1: 30,
            2: 50,
            3: 100,
            4: 200,
            5: 500,
            6: 1000,
            7: 2000,
            8: 3000,
        }

        try:
            if chargetype > 8:
                coin = int(coin_form.cleaned_data['charge'])
            else:
                coin = switch[chargetype]*100
        except:
            coin = 0

        orginmoney = int(coin)
        money = int(coin*precent/100)
        ordertype = ""
        if chargetype > 9:
            ordertype = "1" + str(chargetype)
        else:
            ordertype = "10" + str(chargetype)

        if coin <= 0 | len(ordertype) == 0:
            errortype = -2
            return render(request, 'chargetran.html', {"chargetype": errortype, "success": success})


        nonce_str = random_str()  # 拼接出随机的字符串即可，我这里是用  时间+随机数字+5个随机字母

        total_fee = money  # 付款金额，单位是分，必须是整数 1:1 测试用1分
        body = '缝芽币充值'  # 商品描述
        out_trade_no = order_num(ordertype,username)  # 订单编号

        params = {
            'appid': _APP_ID,  # APPID
            'mch_id': _MCH_ID,  # 商户号
            'nonce_str': nonce_str,  # 回调地址
            'out_trade_no': out_trade_no,  # 订单编号
            'total_fee': total_fee,  # 订单总金额
            'spbill_create_ip': _CREATE_IP,  # 发送请求服务器的IP地址
            'notify_url': _NOTIFY_URL,  # 支付回调地址
            'body': body,  # 商品描述
            'trade_type': 'NATIVE'  # 扫码支付
        }

        sign = get_sign(params, _API_KEY)  # 获取签名
        params['sign'] = sign  # 添加签名到参数字典

        xml = trans_dict_to_xml(params)  # 转换字典为XML
        response = requests.request('post', _UFDODER_URL, data=xml.encode())  # 以POST方式向微信公众平台服务器发起请求
        data_dict = trans_xml_to_dict(response.content)  # 将请求返回的数据转为字典
        qrcode_name = out_trade_no + '.png'  # 支付二维码图片保存路径

        if data_dict.get('return_code') == 'SUCCESS':  # 如果请求成功
            #获取成功写入orderstart
            try:
                new_orderstart = models.OrderStart.objects.create(orderid=out_trade_no, coin=coin, money=money,userid=username, precent=precent,orginmenoy=orginmoney)
                new_orderstart.save();
            except:
                errortype = -2
                return render(request, 'chargetran.html', {"chargetype": errortype, "success": success})

            img = qrcode.make(data_dict.get('code_url'))  # 创建支付二维码片
            img.save('static' + '/qrcode/' + qrcode_name)  #
            qrcodepath = '/qrcode/' + qrcode_name
            return render(request, 'pay.html', {'qrcodepath': qrcodepath,'orderid':out_trade_no})  # 为支付页面模板传入二维码图像

        errortype = -3
        return render(request, 'chargetran.html', {"chargetype": errortype, "success": success})
    else:
        return redirect('/index/')



# 支付成功后回调
@csrf_exempt  # 去除csrf验证
def check_wxpay(request):
    data_dict = trans_xml_to_dict(request.body)  # 回调数据转字典

    try:
        sign = data_dict.pop('sign')  # 取出签名
        key = _API_KEY  # 商户交易密钥
        back_sign = get_sign(data_dict, key)  # 计算签名
        if sign == back_sign:  # 验证签名是否与回调签名相同
            # 先写入再删除
            params = {
                'return_code': 'SUCCESS',
                'return_msg': 'OK',
            }

            xml = trans_dict_to_xml(params)  # 转换字典为XML
            orderstate = 0
            strresult = str(data_dict.pop('result_code'))
            if strresult == "SUCCESS":              
                orderstate = 1

            try:
                out_trade_no = data_dict.pop('out_trade_no')
                wechatid = data_dict.pop('transaction_id')
                order_start = models.OrderStart.objects.get(orderid=out_trade_no)
                meony = order_start.money
                returnmeony = int(data_dict.pop('cash_fee'))
                if meony != returnmeony:
                    orderstate = 0

                coin = order_start.coin
                username = order_start.userid
                UserCheck = models.Commonuser.objects.get(userid=username)
                md5 = UserCheck.binduser

                if len(md5 <= 0):
                    new_orderover = models.OrderOver.objects.create(orderid=out_trade_no, coin=order_start.coin,
                                                                    money=order_start.money, userid=order_start.userid,
                                                                    precent=order_start.precent, orderstate=orderstate,
                                                                    wechatid=wechatid)
                    new_orderover.save()
                else:
                    BindUser = models.Commonuser.objects.get(md5=md5)
                    spreadprecent = BindUser.spreadprecent
                    dividemoney = int(order_start.orginmenoy)*spreadprecent/100
                    new_orderover = models.OrderOver.objects.create(orderid=out_trade_no, coin=order_start.coin,
                                                                    money=order_start.money, userid=order_start.userid,
                                                                    precent=order_start.precent, orderstate=orderstate,
                                                                    wechatid=wechatid, binduser=md5,
                                                                    spreadprecent=spreadprecent,
                                                                    dividemoney=dividemoney)
                    new_orderover.save()


                order_start.delete()

                # 订单都操作完成后操作用户账户
                if orderstate == 1:
                    User = models.Commonuser.objects.get(userid=username)
                    fengyacoin = User.fengyacoin + coin
                    models.Commonuser.objects.filter(userid=username).update(fengyacoin=fengyacoin)
                    coinadd = 0 - coin
                    opratecoinpool(coinadd)
                # 减少存储空间删除二维码图片
                qrcode_name = out_trade_no + '.png'  # 支付二维码图片保存路径
                qrcodepath = os.path.join('static' + '/qrcode/', qrcode_name)
                os.remove(qrcodepath)
                return HttpResponse(xml)
            except:
                return HttpResponse(xml)
        else:
            return HttpResponse('签名验证失败')
    except:
        return HttpResponse('参数错误')

#获取签名
def get_sign(data_dict, key):  # 签名函数，参数为签名的数据和密钥
    params_list = sorted(data_dict.items(), key=lambda e: e[0], reverse=False)  # 参数字典倒排序为列表
    params_str = "&".join(u"{}={}".format(k, v) for k, v in params_list) + '&key=' + key
    # 组织参数字符串并在末尾添加商户交易密钥
    md5 = hashlib.md5()  # 使用MD5加密模式
    md5.update(params_str.encode())  # 将参数字符串传入
    sign = md5.hexdigest().upper()  # 完成加密并转为大写
    return sign

#生成订单号
def order_num(package_id=101, user_id=56789):
    # 商品id后2位+下单时间的年月日12+用户2后四位+随机数4位  商品id第一位1充值2积分后面代表种类三位各位补0，用户ID可以带英文
    local_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))[2:]
    result = str(package_id) + local_time + str(user_id)[-4:] + str(random.randint(100000, 999999))
    return result

#生成提现订单号
def cash_num(package_id=10, user_id=56789):#10微信提现；20银行卡提现
    local_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))[2:]
    result = str(package_id) + local_time + str(user_id)[-5:] + str(random.randint(100000, 999999))
    return result

#生成随机字符串
def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str

def opratecoinpool(coin = 0):
    coinpool = models.CoinPool.objects.get(primaryid='totalcoin')
    coinpool.totalcoin = F('totalcoin') + coin
    coinpool.save()
    return


def check_test(request):
       orderstate = 1
       try:
           out_trade_no = "106190902012015ercc744699"
           wechatid = "ceshicehiscehis"
           order_start = models.OrderStart.objects.get(orderid=out_trade_no)
           meony = order_start.money
           returnmeony = 100000
           if meony != returnmeony:
               orderstate = 0

           coin = order_start.coin
           username = order_start.userid
           new_orderover = models.OrderOver.objects.create(orderid=out_trade_no, coin=order_start.coin,
                                                           money=order_start.money, userid=order_start.userid,
                                                           precent=order_start.precent, orderstate=orderstate,
                                                           wechatid=wechatid)
           new_orderover.save()
           order_start.delete()

           # 订单都操作完成后操作用户账户
           if orderstate == 1:
               User = models.Commonuser.objects.get(userid=username)
               fengyacoin = User.fengyacoin + coin
               models.Commonuser.objects.filter(userid=username).update(fengyacoin=fengyacoin)
               coinadd = 0 - coin
               opratecoinpool(coinadd)
           #减少存储空间删除二维码图片
           qrcode_name = out_trade_no + '.png'  # 支付二维码图片保存路径
           qrcodepath = os.path.join('static' + '/qrcode/', qrcode_name)
           os.remove(qrcodepath)
           return HttpResponse('测试成功')
       except:
            return HttpResponse('测试失败')

#获取推链接md5网址
def get_md5(username):
    src = "darksnl" + username
    m1 = hashlib.md5()
    m1.update(src.encode('utf-8'))
    return m1.hexdigest()

def get_spreadqrcode(spreadurl,username):

    qrcodepath = ""
    try:
        qrcode_name = username + '.png'  # 支付二维码图片保存路径
        img = qrcode.make(spreadurl)  # 创建支付二维码片
        img.save('static' + '/spreadqrcode/' + qrcode_name)
        qrcodepath = '/spreadqrcode/' + qrcode_name
        return qrcodepath
    except:
        return qrcodepath

def replace_username(username):
    str = username[0:3] + "****" + username[-2]
    return str

def replace_realname(realname):
    length = len(realname)
    str = realname[0:1]
    if length > 2:
        for i in range(1,length - 1):
            str += "*"
        str += realname[-1]
    else:
        str += "*"
    return str

def replace_cardid(carid):
    length = len(carid)
    str = carid[0:5] + "***********" + carid[-2:]
    return str

def judge_cardid(cardid):
    ID_check = cardid[17]
    W = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    ID_num = [18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
    ID_CHECK = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
    ID_aXw = 0
    for i in range(len(W)):
        ID_aXw = ID_aXw + int(cardid[i]) * W[i]

    ID_Check = ID_aXw % 11
    if ID_check != ID_CHECK[ID_Check]:
        return False
    else:
        return True

def wechatauthorizefile(request):
    return render(request, "MP_verify_7AKOcVh5wQ73jMyU.txt")

def wechatauthorizeqrcode(userid):
    return_uri = "https://www.yuntaoz.cn/wechatbind/"
    url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=" + _APP_ID + "&redirect_uri=" + return_uri + "&response_type=code&scope=snsapi_userinfo&state=" + userid + "#wechat_redirect"
    qrcode_name = userid + '.png'
    img = qrcode.make(url)  # 创建支付二维码片
    img.save('static' + '/qrcode/' + qrcode_name)  #
    qrcodepath = '/qrcode/' + qrcode_name
    return qrcodepath

def get_bindwechat_userinfo(code):
    token_url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid="+ _APP_ID + "&secret=" +_API_KEY +"&code=" + code + "&grant_type=authorization_code"
    response = requests.request('get', token_url)
    data_dict = json.loads(response.content)  # 将请求返回的数据转为字典
    openid = data_dict.get("openid","")
    access_token = data_dict.get("access_token","")

    if len(openid) == 0 | len(access_token) == 0:
        return  {"errorcode":-1,"errormessage":"获取用户openid失败，请重新扫码绑定！"}

    user_url = "https://api.weixin.qq.com/sns/userinfo?access_token="+ access_token +"&openid="+ openid + "&lang=zh_CN"

    responseuser = requests.request('get', user_url)
    user_data_dict = json.loads(responseuser.content)  # 将请求返回的数据转为字典
    subscribe = user_data_dict.get("subscribe",-1)
    if subscribe < 0:
        return  {"errorcode":-2,"errormessage":"获取用户关注信息失败，请重新扫码绑定！"}
    elif subscribe == 0:
        return {"errorcode":-3,"errormessage":"您尚未关注石缝芽数据微信公众号，请关注后重新扫码绑定！"}

    return {"errorcode":0, "errormessage": "SUCCESS","openid":openid}

#微信提现接口
def wechatcash(realname,cash,trade_no,openid,userid):
    nonce_str = random_str()
    params = {
        'mch_appid': _APP_ID,  # APPID
        'mchid': _MCH_ID,  # 商户号
        'nonce_str': nonce_str,  # 回调地址
        'partner_trade_no': trade_no,  # 订单编号
        'openid':openid,
        'check_name':'FORCE_CHECK',
        're_user_name':realname,
        'amount':cash,
        'desc':'渠道分成提现',
        'spbill_create_ip':_CREATE_IP
    }

    sign = get_sign(params, _API_KEY)  # 获取签名
    params['sign'] = sign  # 添加签名到参数字典

    xml = trans_dict_to_xml(params)  # 转换字典为XML
    response = requests.request('post', _PAYMENT_URL, data=xml.encode())  # 以POST方式向微信公众平台服务器发起请求
    data_dict = trans_xml_to_dict(response.content)

    return_code = data_dict.get("return_code","")

    if return_code == "SUCCESS":
        result_code = data_dict.get("result_code","")
        if result_code == "SUCCESS":
            payment_no = data_dict.get("payment_no","")
            try:
                models.CashOrder.objects.filter(orderid=trade_no).update(orderstate=1, appeal=0,wechatpayno=payment_no)
            except:
                return
        else:
            err_code = data_dict.get("err_code", "")
            if len(err_code) == 0:
                try:
                    models.CashOrder.objects.filter(orderid=trade_no).update(orderstate=-1, appeal=0)
                except:
                    return
                return

            if err_code == "FREQ_LIMIT":
                return

            err_code_des = ""
            err_code_des = usererror_dict.get(err_code, "")

            if len(err_code_des) != 0:
                try:
                    models.CashOrder.objects.filter(orderid=trade_no).update(orderstate=0,failreson=err_code_des,usererror=1,appeal=0)
                    retospreaduserpay(userid,cash)
                except:
                    return
                return

            err_code_des = syserror_dict.get(err_code, "")
            if len(err_code_des) != 0:
                try:
                    models.CashOrder.objects.filter(orderid=trade_no).update(orderstate=0, failreson=err_code_des, appeal=0)
                    retospreaduserpay(userid, cash)
                except:
                    return
                return

            err_code_des = retryerror_dict.get(err_code, "")

            if len(err_code_des) != 0:
                try:
                    order =  models.CashOrder.objects.get(orderid=trade_no)
                    order.orderstate = 3
                    order.rechecktimes = order.rechecktimes + 1
                    order.save()
                except:
                    return

            #未识别错误直接状态不明
            try:
                models.CashOrder.objects.filter(orderid=trade_no).update(orderstate=-1, appeal=0)
            except:
                return
    else:
        return_msg = data_dict.get("return_msg","")
        try:
            models.CashOrder.objects.filter(orderid=trade_no).update(orderstate=0, failreason=return_msg)
        except:
            return
        return


#微信查询接口
def researchcash(userid,trade_no,cash):
    nonce_str = random_str()
    params = {
        'nonce_str': nonce_str,
        'partner_trade_no': trade_no,  # 订单编号
        'mch_id': _MCH_ID,  # 商户号
        'appid': _APP_ID,  # APPID
    }

    sign = get_sign(params, _API_KEY)  # 获取签名
    params['sign'] = sign  # 添加签名到参数字典

    xml = trans_dict_to_xml(params)  # 转换字典为XML
    response = requests.request('post', _PAYMENTCHECK_URL, data=xml.encode())  # 以POST方式向微信公众平台服务器发起请求
    data_dict = trans_xml_to_dict(response.content)

    return_code = data_dict.get("return_code","")

    if return_code == "SUCCESS":
        result_code = data_dict.get("result_code","")

        if result_code == "SUCCESS":
            status = data_dict.get("status","")
            if status == "SUCCESS":
                try:
                    payment_no = data_dict.get("detail_id","")
                    models.CashOrder.objects.filter(orderid=trade_no).update(orderstate=1, appeal=0, wechatpayno=payment_no)
                except:
                    return
            elif status == "FAILED":
                try:
                    reason = data_dict.get("reason", "")
                    models.CashOrder.objects.filter(orderid=trade_no).update(orderstate=0, failreson=reason, appeal=0)
                    retospreaduserpay(userid, cash)
                except:
                    return
            elif status == "PROCESSING":
                return
        else:
            # 特殊需要处理未找到单号重试
            err_code = data_dict.get("err_code", "")
            if err_code == "NOT_FOUND":
                try:
                    models.CashOrder.objects.filter(orderid=trade_no).update(orderstate=2)
                except:
                    return
            return
    else:
        return

#批量提现执行接口，每两秒执行30次
def excutewechatcash():
    cashorder_list = []
    cashorder_list = models.CashOrder.objects.filter(iswechat=1,orderstate=2,rechecktimes__lt=3).order_by("time")[:30]
    for order in cashorder_list:
        wechatcash(order.realname,order.meony,order.orderid,order.openid,order.userid)
    return

#批量查询提现执行接口，对不明状态或非正常失败订单进行重查，有必要重新支付的改写数据库，确认失败的改写数据库，10分钟一次
def excuteresearch():
    retryorder_list = []
    retryorder_list = models.CashOrder.objects.filter(iswechat=1, orderstate=3).order_by("time")
    for order in retryorder_list:
        if order.rechecktimes >= 3:
            try:
                models.CashOrder.objects.filter(orderid=order.orderid).update(orderstate=-1, appeal=0)
                continue
            except:
                continue
        researchcash(order.userid, order.orderid, order.meony)

    return


def retospreaduserpay(userid,cash):
    try:
        BindUser = models.CashBind.objects.get(userid=userid)
        BindUser.wechateverydaytimes = BindUser.wechateverydaytimes + 1
        BindUser.wechattimes = BindUser.wechattimes + 1
        BindUser.save()

        User = models.Commonuser.objects.get(userid=userid)
        User.spreadmeony = F('spreadmeony') + cash
        User.save()
    except:
        return

def recoverdaytimes():
    try:
        models.CashBind.objects.all().update(wechateverydaytimes=1)
        models.Commonuser.objects.all().update(appstate=0)
    except:
        return
    return

def recovermonthtimes():
    try:
        models.CashBind.objects.all().update(wechattimes=3, banktimes=2)
    except:
        return
    return


#三方平台使用
#获取票据ticket，微信每十分钟推送一次
def openweixin(request):
    #获取加密数据解密，然后将时间戳与ticket存入数据库
    #若失败不更新，ticket有效时间较长
    if request.method == "POST":
        #query = request.query_params
        nonce = request.GET.get('nonce', "")
        timestamp = request.GET.get('timestamp', "")
        msg_sign = request.GET.get('msg_signature', "")
        #postdata
        encrypt_xml = str(request.body)
        #encrypt_xml = '<xml>\n <AppId><![CDATA[wxc0ad5e0f7a6d4e4f]]></AppId>\n <Encrypt><![CDATA[bWdLrJBJReLB2411DEdZeGY+0BZO82xtS2lfBpInw5vRkCNNXs9qHUVXMuMoSUePSbvVefhSZIHAscvBU1DIVg4iCsoZoGnhosejrJVKM2BBtnu47exqJsJkwFnwVu5VvsfRl95yDBu16SyvjWALJmMJOBawKiW1YcCrj9VnjFcvqXXa1vEMo1g6J/yoiTrUWStprQZXuUz5HVn6UV3klDUrclvRAdS9lL5NV14XoAQwAYab+8Yk1gXVxHZYURGv96UTHoauma4fEh1VmwinsHBTrnnBCTWvJ39KWiUhNVOjo5LdGLa0e+dMh9OUsJbjjbBWE+8nU4soSdalVYknowuYvwkZzYJnOy+wpZOqHjE//8hHnPKIF8kef7EZHrFbqMPqPLuy8GPftEM7HJo6dgVX5Xrr+0emcD+3B1/rqiU/ZxRgQtl3bvF9a9VeNf6EEtQhzm+sN3xbtmdZVvukrQ==]]></Encrypt>\n </xml>\n'
        decrypt_test = WXBizMsgCrypt(component_tocken, encodingAESKey,component_appid)
        ret, decryp_xml = decrypt_test.DecryptMsg(encrypt_xml, msg_sign, timestamp, nonce)
        #print(decryp_xml)
        if ret != 0:#解密报错，打印log
            return HttpResponse("success")
        else:#解密成功写入数据库
            #将xml解析为dict
            dict = trans_xml_to_dict(decryp_xml)
            infotype = dict.get("InfoType","")

            if infotype == "component_verify_ticket":
                appid = dict.get("AppId", "")
                createtime = int(dict.get("CreateTime", 0))
                ticket = dict.get("ComponentVerifyTicket", "")

                if appid != component_appid:
                    return HttpResponse("success")

                if len(ticket) == 0 or createtime == 0:
                    return HttpResponse("success")

                try:
                    component = models.ComponentInfo.objects.get(componentappid=component_appid)
                    component.componentverifyticket = ticket
                    component.tickettime = createtime
                    component.save()
                except:
                    try:
                        component = models.ComponentInfo.objects.create(componentappid=component_appid,
                                                                        componentverifyticket=ticket,
                                                                        tickettime=createtime)
                        component.save()
                    except:
                        return HttpResponse("success")

                return HttpResponse("success")
            else:
                return HttpResponse("success")
            #添加取消授权功能，已授权公众号不在保留



#通过ticket获取tocken ；定时1分钟;读取数据库token时间，100分钟以上更新
def get_plattocken():
    try:
        component = models.ComponentInfo.objects.get(componentappid=component_appid)
        tockentime = component.tockentime
        nowstamp = int(time.time())
        if nowstamp - tockentime > 6000:
            #获取tocken
            ticket = component.componentverifyticket
            tockenurl = "https://api.weixin.qq.com/cgi-bin/component/api_component_token"
            dict = {"component_appid": component_appid, "component_appsecret": component_secret, "component_verify_ticket": ticket}
            postdata = str(dict)
            response = requests.request('post', tockenurl, data=postdata.encode())  # 以POST方式向微信公众平台服务器发起请求
            content = response.content
            tocken_dict = eval(content)
            tocken = tocken_dict.get("component_access_token", "")
            if len(tocken) > 0:
                nowtockentime = int(time.time())
                component.tockentime = nowtockentime
                component.componentaccesstoken = tocken
                component.save()
                return
            return
        else:
            return
    except:
        return

#获取预授权码；调用的时候在获取即可，有效时限10分钟
def get_pre_auth_code():
    code = ""
    try:
        component = models.ComponentInfo.objects.get(componentappid=component_appid)
        tockentime = component.tockentime
        nowstamp = int(time.time())
        if nowstamp - tockentime < 6600:
            tocken = component.componentaccesstoken
            url = "https://api.weixin.qq.com/cgi-bin/component/api_create_preauthcode?component_access_token=" + tocken
            dict = {"component_appid": component_appid}
            postdata = str(dict)
            response = requests.request('post', url, data=postdata.encode())  # 以POST方式向微信公众平台服务器发起请求
            content = response.content
            code_dict = eval(content)
            code = code_dict.get("pre_auth_code", "")
            return code
        else:
            return code
    except:
        return code


#获取公众号授权回调二维码
def call_back_authorize_qrcode(userid):
    uri = "https://www.yuntaoz.cn/palt/authorizecallback/" + userid + "/"
    code = get_pre_auth_code()
    success = 0
    if(len(code) == 0):
       return success,""

    url = "https://mp.weixin.qq.com/cgi-bin/componentloginpage?component_appid=" + component_appid + \
          "&pre_auth_code="+ code +"&redirect_uri=" + uri +"&auth_type=1" #当前只展示公众号

    qrcode_name = userid + '.png'
    img = qrcode.make(url)
    img.save('static' + '/authorizeqrcode/' + qrcode_name)#是否回覆盖原文件需要测试一下（必须覆盖，因为每次code不相同可能），10分钟提醒用户更新图片
    qrcodepath = '/authorizeqrcode/' + qrcode_name
    success = 1
    return success,qrcodepath


#微信公众号授权回调
def call_back_authorize(request,userid):
    auth_code = request.GET.get("auth_code","")

    if len(auth_code) <= 0 or len(userid) <= 0:
        return HttpResponse("对不起，您的授权失败，请重新进行授权！")

    try:
        component = models.ComponentInfo.objects.get(componentappid=component_appid)
        tockentime = component.tockentime
        nowstamp = int(time.time())
        if nowstamp - tockentime < 6600:
            tocken = component.componentaccesstoken
            url = "https://api.weixin.qq.com/cgi-bin/component/api_query_auth?component_access_token=" + tocken
            dict = {"component_appid": component_appid, "authorization_code":auth_code}
            postdata = str(dict)
            response = requests.request('post', url, data=postdata.encode())  # 以POST方式向微信公众平台服务器发起请求
            content = response.content
            user_dict = trans_xml_to_dict(content)
            authorizer_appid = user_dict.get("authorizer_appid", "")
            authorizer_access_token = user_dict.get("authorizer_access_token", "")
            authorizer_refresh_token = user_dict.get("authorizer_refresh_token", "")
            nowtockentime = int(time.time())

            try:#在用户绑定界面时，就判断是否被别的账号绑定，或已经绑定
                authorizeinfo = models.AuthorizeInfo.objects.get(appid=authorizer_appid)
                useridalready = authorizeinfo.userid
                type = authorizeinfo.type
                if type == 1:
                    ret = get_app_info(authorizer_appid,tocken)
                    if useridalready == userid:
                        if ret == 0:
                            return HttpResponse("该公众号已绑定成功，但是未拉取到公众号信息，不能使用平台增粉功能，您可以解除授权后重新授权，很抱歉给您带来的麻烦!")

                        return HttpResponse("该公众号已绑定成功，可以使用增粉功能，请刷新平台授权页面后查看!")
                    else:
                        return HttpResponse("该公众号已绑定其他推广用户，请解除授权后重试!")
                else:
                    models.AuthorizeInfo.objects.filter(userid=userid).update(type=-3)
                    authorizeinfo.userid = userid
                    authorizeinfo.type = 1
                    authorizeinfo.accesstoken = authorizer_access_token
                    authorizeinfo.refreshtoken = authorizer_refresh_token
                    authorizeinfo.tockentime = nowtockentime
                    authorizeinfo.save()
                    ret = get_app_info(authorizer_appid,tocken)
                    if ret == 0:
                        return HttpResponse("该公众号已绑定成功，但是未拉取到公众号信息，不能使用平台增粉功能，您可以解除授权后重新授权，很抱歉给您带来的麻烦!")
                    return HttpResponse("恭喜您，公众号授权成功，可以使用增粉功能，请刷新平台授权页面后查看!")#授权u页面也进行提示
            except:
                try:
                    models.AuthorizeInfo.objects.filter(userid=userid).update(type=-3)
                    authorizeinfo = models.AuthorizeInfo.objects.create(appid=authorizer_appid, userid=userid,
                                                                        accesstoken=authorizer_access_token,
                                                                        refreshtoken=authorizer_refresh_token,
                                                                        tockentime=nowtockentime, type=1)
                    authorizeinfo.save()
                    ret = get_app_info(authorizer_appid, tocken)
                    if ret == 0:
                        return HttpResponse("该公众号已绑定成功，但是未拉取到公众号信息，不能使用平台增粉功能，您可以解除授权后重新授权，很抱歉给您带来的麻烦!")
                    return HttpResponse("恭喜您，公众号授权成功，可以使用增粉功能!")
                except:
                    return HttpResponse("对不起，由于网站系统超时，您的授权失败，请稍后重新进行授权,若显示已授权，请解除授权后重试!")
        else:
            return HttpResponse("对不起，由于网站系统超时，您的授权失败，请稍后重新进行授权,若显示已授权，请解除授权后重试!")
    except:
        return HttpResponse("对不起，由于网站系统问题，您的授权失败，请稍后重新进行授权,若显示已授权，请解除授权后重试!")

#获取公众号信息写入数据库
def get_app_info(appid,tocken):
    url = "https://api.weixin.qq.com/cgi-bin/component/api_get_authorizer_info?component_access_token=" + tocken
    dict = {"component_appid": component_appid, "authorizer_appid": appid}
    postdata = str(dict)
    response = requests.request('post', url, data=postdata.encode())  # 以POST方式向微信公众平台服务器发起请求
    content = response.content
    info_dict = trans_xml_to_dict(content)
    authorization_info_dict = info_dict.get("authorizer_info")
    nickname = authorization_info_dict.get("nick_name","")
    headimg = authorization_info_dict.get("head_img","")
    qrcodeurl = authorization_info_dict.get("qrcode_url","")
    principal_name = authorization_info_dict.get("principal_name","")
    signature = authorization_info_dict.get("signature","")#公众号介绍，直接获取
    id = authorization_info_dict.get("service_type_info","").get("id",-1)
    serviceinfo = ""
    if id == 0:
        serviceinfo = "订阅号"
    elif id == 1:
        serviceinfo = "订阅号"
    elif id == 2:
        serviceinfo = "服务号"
    else:
        serviceinfo = "未知"

    ret = 1
    if len(nickname) == 0 | len(headimg) == 0 | len(qrcodeurl) == 0:
       ret = 0
       return ret

    try:
        authorizeinfo = models.AuthorizeInfo.objects.get(appid=appid)
        authorizeinfo.nick_name = nickname
        authorizeinfo.head_img = headimg
        authorizeinfo.service_type = serviceinfo
        authorizeinfo.qrcode_url = qrcodeurl
        authorizeinfo.principal = principal_name
        authorizeinfo.describe = signature
    except:
        ret = 0

    return ret






#刷新公众号授权令牌
def get_refresh_tocken(authorizer_appid):
    str = ""
    errornum = 0
    if len(authorizer_appid) > 0:
        nowstamp = int(time.time())
        refreshtoken = ""
        try:
            authorizeinfo = models.AuthorizeInfo.objects.get(appid=authorizer_appid)
            refreshtoken = authorizeinfo.refreshtoken
            usertimestamp = authorizeinfo.tockentime
            if nowstamp - usertimestamp < 6600:
                str = authorizeinfo.accesstoken
                errornum = 10001
                return str, errornum
        except:
            errornum = -10002  # 数据库出错
            return str, errornum

        try:
            component = models.ComponentInfo.objects.get(componentappid=component_appid)
            tockentime = component.tockentime

            if nowstamp - tockentime < 6600:
                tocken = component.componentaccesstoken
                url = "https://api.weixin.qq.com/cgi-bin/component/api_authorizer_token?component_access_token=" + tocken
                dict = {"component_access_token": tocken, "component_appid": component_appid, "authorizer_appid":authorizer_appid, "authorizer_refresh_token":refreshtoken}
                postdata = str(dict)
                response = requests.request('post', url, data=postdata.encode())  # 以POST方式向微信公众平台服务器发起请求
                content = response.content
                user_dict = eval(content)
                authorizer_access_token = user_dict.get("authorizer_access_token", "")
                nowtockentime = int(time.time())
                try:
                    models.AuthorizeInfo.objects.filter(appid=authorizer_appid).update(accesstoken=authorizer_access_token,tockentime=nowtockentime)
                    str = authorizer_access_token
                    errornum = 10002
                    return str, errornum
                except:
                    str = authorizer_access_token
                    errornum = 10003  # 数据库出错,但返回了公众号tocken
                    return str, errornum
            else:
                errornum = -10003  # 三方平台tocken超时
                return str, errornum
        except:
            errornum = -10002#数据库出错
            return str,errornum
    else:
        errornum = -10001#参数传递错误
        return str, errornum



#授权网址#代公众号网页授权
def get_authorize_url_qrcode(appid,userid):#appid：推广公众号id；userid：推广用户id
    return_uri = "https://www.yuntaoz.cn/plat/componentauthorize/" + userid + "/"
    url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid="+ appid +"&redirect_uri="+ return_uri +"&response_type=code&scope=snsapi_userinfo&state="+ userid +"component_appid="+ component_appid +"#wechat_redirect"

    qrcode_name = appid + userid + '.png'
    img = qrcode.make(url)  # 创建支付二维码片
    img.save('static' + '/componentqrcode/' + qrcode_name)  #
    qrcodepath = '/componentqrcode/' + qrcode_name
    return qrcodepath

#授权网址#代公众号网页授权,文章
def get_authorize_url_article_qrcode(appid,userid,title):#appid：推广公众号id；userid：推广用户id
    return_uri = "https://www.yuntaoz.cn/plat/componentauthorizearticle/" + userid + "/" + title + "/"
    url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid="+ appid +"&redirect_uri="+ return_uri +"&response_type=code&scope=snsapi_userinfo&state="+ userid +"component_appid="+ component_appid +"#wechat_redirect"

    qrcode_name = appid + userid + 'article.png'
    img = qrcode.make(url)  # 创建支付二维码片
    img.save('static' + '/componentqrcode/' + qrcode_name)  #
    qrcodepath = '/componentqrcode/' + qrcode_name
    return qrcodepath

def isequaldate(date):
    if not date:
        return 0

    beforedate = datetime.strptime(date, '%Y-%m-%d')
    nowdate = timezone.now().strftime("%Y-%m-%d")
    trandate = datetime.strptime(nowdate, '%Y-%m-%d')

    delta = trandate - beforedate
    interval = delta.days
    if interval == 0:
        return 1
    else:
        return 0

def get_palt_tocken(component_appid):
    str = ""
    errornum = 0
    if len(component_appid) > 0:
        nowstamp = int(time.time())
        refreshtoken = ""

        try:
            component = models.ComponentInfo.objects.get(componentappid=component_appid)
            tockentime = component.tockentime
            nowstamp = int(time.time())
            if nowstamp - tockentime > 6000:
                # 获取tocken
                ticket = component.componentverifyticket
                tockenurl = "https://api.weixin.qq.com/cgi-bin/component/api_component_token"
                dict = {"component_appid": component_appid, "component_appsecret": component_secret,
                        "component_verify_ticket": ticket}
                postdata = str(dict)
                response = requests.request('post', tockenurl, data=postdata.encode())  # 以POST方式向微信公众平台服务器发起请求
                content = response.content
                tocken_dict = eval(content)
                tocken = tocken_dict.get("component_access_token", "")
                if len(tocken) > 0:
                    nowtockentime = int(time.time())
                    component.tockentime = nowtockentime
                    component.componentaccesstoken = tocken
                    component.save()
                    str = tocken
                    return str,errornum

                errornum = -10001#刷新tocken失败
                return str,errornum
            else:
                tocken = component.componentaccesstoken
                str = tocken
                return str, errornum
        except:
            errornum = -10002  # 查询tocken失败，查询数据库失败
            return str, errornum

#用户关注公众号回调
def authorize_user_code(request,userid):
    code = request.GET.get("code", "")
    userid = request.GET.get("state", "")
    appid = request.GET.get("appid", "")
    success = 1
    if len(code) == 0 or len(appid) == 0:
        success = 0
        return render(request, 'authorizeuserinfo.html', locals())

    authorize_user_result(request, code, userid, appid)

def authorize_user_result(request,code,userid,appid):

    if len(code) == 0 or len(appid) == 0 or len(userid) == 0:
        success = 0
        return render(request, 'authorizeuserinfo.html', locals())

    tocken,errornum = get_palt_tocken()

    if errornum < 0:
        return render(request, 'authorizeuserresult.html', {"sign":-3})

    token_url = "https://api.weixin.qq.com/sns/oauth2/component/access_token?appid=" + appid + "&code="+ code + "&grant_type=authorization_code&component_appid=" + component_appid + "&component_access_token=" + tocken
    response = requests.request('get', token_url)
    data_dict = json.loads(response.content)  # 将请求返回的数据转为字典
    openid = data_dict.get("openid", "")
    access_token = data_dict.get("access_token", "")

    if len(openid) == 0 | len(access_token) == 0:
        return render(request, 'authorizeuserresult.html', {"sign":0})

    user_url = "https://api.weixin.qq.com/sns/userinfo?access_token=" + access_token + "&openid=" + openid + "&lang=zh_CN"

    responseuser = requests.request('get', user_url)
    user_data_dict = json.loads(responseuser.content)  # 将请求返回的数据转为字典
    subscribe = user_data_dict.get("subscribe", -1)
    if subscribe < 0:
        return render(request, 'authorizeuserresult.html', {"sign": 0})
    elif subscribe == 0:
        return render(request, 'authorizeuserresult.html', {"sign": -1})

    #处理领取缝芽币，防止以重复领取，用户界面勿忘领取过不在显示二维码
    try:
        User = models.Commonuser.objects.get(userid = userid)
        giftdate = User.fengyadate
        if len(giftdate) != 0:
            alreadyget = isequaldate(giftdate)
            if alreadyget == 1:
                return render(request, 'authorizeuserresult.html', {"sign": -2})

        # 记录已关注公众号,记录出错不可领取缝芽币，稍后领取
        try:
            concern = models.ConcernInfo.objects.create(appid=appid, userid=userid)
            concern.save()
        except:
            return render(request, 'authorizeuserresult.html', {"sign": -3})

        #赠送缝芽币不进入pool，但是有订单生成，表示赠送
        #赠送
        User.fengyadate = timezone.now().strftime("%Y-%m-%d")
        User.giftcoin = F('giftcoin') + 500
        User.save()
    except:
        return render(request, 'authorizeuserresult.html', {"sign": -3})

    try:
        # 生成赠送订单（积分赠送也要生成）,102赠送逢芽币
        orderid = order_num(102, userid)
        order = models.OrderOver.objects.create(orderid=orderid,coin=500,userid=userid,orderstate=2,appeal=-1)
        order.save()
    except:
        pass

    return render(request, 'authorizeuserresult.html', {"sign": 1})

#授权变更通知
def authorize_change(request):
    if request.method == "POST":
        nonce = request.GET.get("nonce", "")
        timestamp = request.GET.get("timestamp", "")
        msg_sign = request.GET.get("msg_signature", "")
        # postdata
        encrypt_xml = str(request.body)
        decrypt_test = WXBizMsgCrypt(component_tocken, encodingAESKey, component_appid)
        ret, decryp_xml = decrypt_test.DecryptMsg(encrypt_xml, msg_sign, timestamp, nonce)

        if ret > 0:  # 解密报错，打印log
            return HttpResponse("success")
        else:  # 解密成功写入数据库
            # 将xml解析为dict
            dict = trans_xml_to_dict(decryp_xml)
            infotype = dict.get("InfoType", "")
            AuthorizerAppid = dict.get("AuthorizerAppid", "")
            if(infotype == "unauthorized"):#取消授权
                try:
                    authorizeinfo = models.AuthorizeInfo.objects.get(appid=AuthorizerAppid)
                    authorizeinfo.type = -1
                    authorizeinfo.save()
                except:
                    pass
            elif(infotype == "updateauthorized"):#更新授权
                try:
                    nowtockentime = int(time.time())
                    authorizeinfo = models.AuthorizeInfo.objects.get(appid=AuthorizerAppid)
                    authorizeinfo.type = 1
                    #authorizeinfo.tockentime = nowtockentime#g更新授权可能需要查询新授权是否安祖需求
                    #AuthorizationCode = dict.get("AuthorizationCode", "")
                    #if(len(AuthorizationCode) > 0):
                        #authorizeinfo.accesstoken = AuthorizationCode
                    authorizeinfo.save()
                except:
                    pass
            elif(infotype == "authorized"):#授权
                pass
            return HttpResponse("success")

#用户关注公众号文章回调
def authorize_article(request,userid,title):
    code = request.GET.get("code", "")
    userid = request.GET.get("state", "")
    appid = request.GET.get("appid", "")
    success = 1
    if len(code) == 0 or len(appid) == 0:
        success = 0
        return render(request, 'authorizeuserinfo.html', locals())

    authorize_article_result(request, code, userid, appid, title)

def authorize_article_result(request,code,userid,appid,title):

    if len(code) == 0 or len(appid) == 0 or len(userid) == 0:
        success = 0
        return HttpResponse("对不起，您的授权失败，请重新扫码开通权限，或稍后重试！")

    tocken,errornum = get_palt_tocken()

    if errornum < 0:
        return HttpResponse("十分抱歉，网站数据出错，请稍后重新扫码开通权限！")

    token_url = "https://api.weixin.qq.com/sns/oauth2/component/access_token?appid=" + appid + "&code="+ code + "&grant_type=authorization_code&component_appid=" + component_appid + "&component_access_token=" + tocken
    response = requests.request('get', token_url)
    data_dict = json.loads(response.content)  # 将请求返回的数据转为字典
    openid = data_dict.get("openid", "")
    access_token = data_dict.get("access_token", "")

    if len(openid) == 0 | len(access_token) == 0:
        return HttpResponse("对不起，您的授权失败，请重新扫码开通权限，或稍后重试！")

    user_url = "https://api.weixin.qq.com/sns/userinfo?access_token=" + access_token + "&openid=" + openid + "&lang=zh_CN"

    responseuser = requests.request('get', user_url)
    user_data_dict = json.loads(responseuser.content)  # 将请求返回的数据转为字典
    subscribe = user_data_dict.get("subscribe", -1)
    if subscribe < 0:
        return HttpResponse("对不起，您的尚未关注公众号，请关注后重新扫码开通权限！")
    elif subscribe == 0:
        return HttpResponse("对不起，您的授权失败，请重新扫码开通权限，或稍后重试！")

    #处理开通文章权限
    try:
        arcticlecontain = models.ArticleContain.objects.get(title=title, userid=userid)
        if not arcticlecontain:
            article = models.BlogArticle.objects.get(title=title)
            new_data = models.ArticleContain.objects.create(title=title, userid=userid,
                                                            costtype=article.articlecosttype,
                                                            cost=0, tag=article.tag)
            new_data.save()
    except:
        return HttpResponse("十分抱歉，网站数据出错，请稍后重新扫码开通权限！")

    return HttpResponse("恭喜您，开通权限成功，请您稍后网页自动跳转或后退点击题目阅读文章！")

