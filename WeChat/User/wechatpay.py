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


_APP_ID = "wxb5d226f10420789f"
_MCH_ID = "1543525851"
_API_KEY = "zzhr1990hr0805zjw1991pmf04251111"

_UFDODER_URL = "https://api.mch.weixin.qq.com/pay/unifiedorder" #url是微信下单api
_NOTIFY_URL = "https://www.yuntaoz.cn/checkresult/"
myname = socket.getfqdn(socket.gethostname())
_CREATE_IP = socket.gethostbyname(myname)  # 发起支付请求的ip

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
                new_orderstart = models.OrderStart.objects.create(orderid=out_trade_no, coin=coin, money=money,userid=username, precent=precent)
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
