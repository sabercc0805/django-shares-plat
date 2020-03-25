from django import forms
from captcha.fields import CaptchaField
from DjangoUeditor.forms import UEditorField
from django.forms import widgets
from User import models

class CenterForm(forms.Form):
    trend = forms.ChoiceField(label="今日走势",
       choices=((1, '涨'), (2, '跌'),),  # 定义下拉框的选项，元祖第一个值为option的value值，后面为html里面的值
        initial=1,  # 默认选中第二个option
      widget=forms.RadioSelect  # 插件表现形式为单选按钮
     )
    judge = forms.CharField(label="今日点评",required=False, widget=forms.Textarea(attrs={'class': 'form-control','placeholder': "无点评可以为空",}))
    valueone = forms.FloatField(label="上证指数",widget=forms.NumberInput(attrs={'class': 'form-control'}))
    valuetwo = forms.FloatField(label="模拟仓涨幅",widget=forms.NumberInput(attrs={'class': 'form-control'}))


class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=48, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='验证码',error_messages={'invalid': "验证码错误"})

class UserInfoForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}))
    registertime = forms.CharField(label="注册时间", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}))
    endtime = forms.CharField(label="会员到期时间", max_length=128,
                                   widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    level = forms.CharField(label="会员级别", max_length=128,
                                   widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    coin = forms.CharField(label="缝芽币", max_length=24,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    phonenum = forms.CharField(label="手机号", max_length=11,min_length=11,widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Email",widget=forms.EmailInput(attrs={'class': 'form-control'}))


class ChangePwdForm(forms.Form):
    oldpassword = forms.CharField(
        required=True,
        label="原密码",
        error_messages={'required': "请输入原密码"},
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control','placeholder': "原密码", }), )
    newpassword1 = forms.CharField(
        required=True,
        label=u"新密码",
        error_messages={'required': "请输入新密码"},
        min_length=6,
        max_length=48,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control', 'placeholder': "新密码(长度至少6位)", }), )
    newpassword2 = forms.CharField(
        required=True,
        label=u"确认密码",
        error_messages={'required': "请再次输入新密码"},
        min_length=6,
        max_length=48,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control', 'placeholder': "确认密码", }), )



class RegisterForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=20,min_length=6, widget=forms.TextInput(attrs={'class': 'form-control','placeholder': "用户名长度大于6字符小于20字符，且只能包含字母和数字",}))
    password1 = forms.CharField(label="密码", min_length=8,max_length=48, widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': "密码长度至少大于8位"}))
    password2 = forms.CharField(label="确认密码", min_length=8,max_length=48,widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': "确认密码"}))
    phonenumber = forms.EmailField(label="Email", min_length=5,max_length=48,widget=forms.EmailInput(attrs={'id':'email','class': 'form-control','placeholder': "目前唯一找回密码的验证方式，请认真填写！",}))
    code = forms.CharField(label="激活码", max_length=6,widget=forms.TextInput(attrs={'id':'code','class': 'form-control', 'placeholder': "填入6位激活码", }))
    captcha = CaptchaField(label='验证码',error_messages={'invalid': "验证码错误"})

class ArticleForm(forms.Form):
    articletitle = forms.CharField(label="文章标题",required = True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    articlecontent = UEditorField(label="文章内容",required = True,width=925, height=250)
    right = forms.ChoiceField(label="可查看会员权限",
                              choices=((0, '游客'),(1, '普通会员'),), #(2, '超级会员'),(3, '白金会员'),(4, '钻石会员'),),  # 定义下拉框的选项，元祖第一个值为option的value值，后面为html里面的值
                              initial=1,  # 默认选中第二个option
                              widget=forms.RadioSelect  # 插件表现形式为单选按钮
                              )
    articlecosttype = forms.ChoiceField(label="阅读文章消费类型",
                              choices=((0, '免费'), (1, '积分'),(2, '缝芽币'),),
                              # (2, '超级会员'),(3, '白金会员'),(4, '钻石会员'),),  # 定义下拉框的选项，元祖第一个值为option的value值，后面为html里面的值
                              initial=2,  # 默认选中第二个option
                              widget=forms.RadioSelect  # 插件表现形式为单选按钮
                              )
    articlecost = forms.IntegerField(label="阅读文章消费金额",widget=forms.NumberInput(attrs={'class': 'form-control','defalut':'0'}))
    downloadcosttype = forms.ChoiceField(label="下载附件消费类型",
                                    choices=((0, '免费'), (1, '积分'), (2, '缝芽币'),),
                                    # (2, '超级会员'),(3, '白金会员'),(4, '钻石会员'),),  # 定义下拉框的选项，元祖第一个值为option的value值，后面为html里面的值
                                    initial=2,  # 默认选中第二个option
                                    widget=forms.RadioSelect  # 插件表现形式为单选按钮
                                    )
    cost = forms.IntegerField(label="下载附件消耗缝芽币", widget=forms.NumberInput(attrs={'class': 'form-control', 'defalut': '0'}))
    cancommit = forms.ChoiceField(label="是否可以评论",
                                     initial=1,
                                     choices=((0, '否'), (1, '是'), (2,'仅作者可回复'),),
                                     # (2, '超级会员'),(3, '白金会员'),(4, '钻石会员'),),  # 定义下拉框的选项，元祖第一个值为option的value值，后面为html里面的值
                                     widget=forms.RadioSelect  # 插件表现形式为单选按钮
                                     )
    #标签
    top = forms.ChoiceField(label="是否置顶",
                                    initial=1,
                                  choices=((0, '否'), (1, '是'),),
                                  # (2, '超级会员'),(3, '白金会员'),(4, '钻石会员'),),  # 定义下拉框的选项，元祖第一个值为option的value值，后面为html里面的值
                                  widget=forms.RadioSelect# 插件表现形式为单选按钮
                                  )
    # 关注公众号免费看
    authorize = forms.ChoiceField(label="是否关注公众号免费",
                                  initial=1,
                            choices=((0, '否'), (1, '是'),),
                            # (2, '超级会员'),(3, '白金会员'),(4, '钻石会员'),),  # 定义下拉框的选项，元祖第一个值为option的value值，后面为html里面的值
                            widget=forms.RadioSelect,  # 插件表现形式为单选按钮
                            )
    tag = forms.IntegerField(label="教程标签",widget=widgets.RadioSelect(),initial=0)
    articletag = forms.CharField(label="标签", max_length=20,required=False,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
    # 保证每次访问重新获取最新数据
    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        choicelist = []
        listadd = [("0","添加标签")]
        choicelist.extend(listadd)
        taglist =  models.BlogTag.objects.values_list("id","name")
        choicelist.extend(taglist)
        size = taglist.count()
        size += 1
        listother = [(str(size),"其他")]
        choicelist.extend(listother)
        print(choicelist)
        self.fields["tag"].widget.choices = choicelist


class Commitform(forms.Form):
    commitcontent = UEditorField(label="评论内容", width=860,required=True,settings={"toolbars":[['undo',
	        		'redo',
	        		'bold',
	        		'indent',
                    'justifyleft',
                    'justifyright',
                    'justifycenter',
                    'justifyjustify',
                    'superscript',
                    'formatmatch',
                    'insertimage',
                    'emotion',
                    'spechars',
	        		'fullscreen']],"maximumWords":1000,},
                                 )
    #commitcontent = forms.CharField(label="评论内容", required=True, min_length=10,max_length=500,widget=forms.Textarea(attrs={
                             # 'id':"commitcontent",'style': 'height: 60px;width:100%;resize:none','placeholder': "评论请大于10字符小于500字符，并且请您的评论遵循国家相关法律法规！",}))

class Creditform(forms.Form):
    exchangetype = forms.ChoiceField(label="兑换选项",
                                    choices=((0, '10积分'), (1, '50积分'), (2, '100积分'),(3, '500积分'),(4, '1000积分'),
                                            (5, '2000积分'),(6, '3000积分'),(7, '5000积分'),),
                                    initial=0,
                                    widget=forms.RadioSelect  # 插件表现形式为单选按钮
                                    )

class Coinform(forms.Form):
    chargetype = forms.ChoiceField(label="充值选项",
                                    choices=((0, '10币'), (1, '30币'), (2, '50币'),(3, '100币'),(4, '200币'),
                                            (5, '500币'),(6, '1000币'),(7, '2000币'),(8, '3000币'),(9, '其他金额'),),
                                    initial=0,
                                    widget=forms.RadioSelect  # 插件表现形式为单选按钮
                                    )
    charge = forms.IntegerField(label="充值金额",min_value=1,max_value=3000,required=False,
                              widget=forms.NumberInput(attrs={'class': 'form-control', 'defalut': '1','placeholder': "请输入大于0，小于3000的整数"}))

class ActiveCodeform(forms.Form):
    precent = forms.IntegerField(label="分成百分比", min_value=1, max_value=70, required=True,
                                widget=forms.NumberInput(
                                    attrs={'class': 'form-control','placeholder': "请输入大于0，小于70的整数"}))

class Activeform(forms.Form):
    code = forms.CharField(label="绑定推广人", max_length=8, min_length=8, required=True,
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control','placeholder': "推广码"}))

class Inviteform(forms.Form):
    code = forms.CharField(label="绑定邀请码", max_length=10, min_length=10, required=True,
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control','placeholder': "邀请码"}))

class RealNameform(forms.Form):
    realname = forms.CharField(label="姓名", max_length=10,min_length=2, required=True,
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control','placeholder': "真实姓名"}))
    cardid = forms.CharField(label="身份证号", max_length=18, min_length=18,required=True,
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control','placeholder': "身份证号"}))

class BankBindform(forms.Form):
    bankid = forms.CharField(label="银行账号", max_length=19,min_length=16,required=True,
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control','placeholder': "输入借记卡账号，长度16-19位"}))
    bankname = forms.CharField(label="银行名称", max_length=10,required=True,
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control','placeholder': "输入银行名称"}))
    code = forms.CharField(label="验证码", max_length=6, widget=forms.TextInput(
        attrs={'id': 'code', 'class': 'form-control', 'placeholder': "填入6位验证码", }))

class BankCashform(forms.Form):
    cash = forms.IntegerField(label="提现金额", min_value=2000, required=True,
                                widget=forms.NumberInput(
                                    attrs={'class': 'form-control', 'defalut': '1','step':'0.01', 'placeholder': "请输大于2000的数值"}))
    code = forms.CharField(label="验证码", max_length=6, widget=forms.TextInput(
        attrs={'id': 'code', 'class': 'form-control', 'placeholder': "填入6位验证码", }))

class WechatCashform(forms.Form):
    cash = forms.IntegerField(label="提现金额", min_value=10, max_value=2000, required=True,
                                widget=forms.NumberInput(
                                    attrs={'class': 'form-control', 'defalut': '1','step':'0.01', 'placeholder': "请输大于10小于2000的数值"}))
    code = forms.CharField(label="验证码", max_length=6, widget=forms.TextInput(
        attrs={'id': 'code', 'class': 'form-control', 'placeholder': "填入6位验证码", }))

class WechatBindform(forms.Form):
    wechatid = forms.CharField(label="微信号", max_length=128, required=False,widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "请填入微信号", }))

class authorizeform(forms.Form):
    appid = forms.CharField(label="APPID", max_length=128, required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "请填入公众号APPID", }))
    appinfo = forms.CharField(label="公众号介绍",required=True, max_length=500,
                              widget=forms.Textarea(attrs={'class': 'form-control','placeholder': "请输入500字以下的公众号简单介绍...",}))

