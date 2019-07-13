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
    username = forms.CharField(label="用户名", max_length=128,min_length=5, widget=forms.TextInput(attrs={'class': 'form-control','placeholder': "用户名长度大于5字符小于20字符",}))
    password1 = forms.CharField(label="密码", max_length=48, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=48,widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    phonenumber = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-control','placeholder': "目前唯一找回密码的验证方式，请认真填写！",}))

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
                                     choices=((0, '否'), (1, '是'),),
                                     # (2, '超级会员'),(3, '白金会员'),(4, '钻石会员'),),  # 定义下拉框的选项，元祖第一个值为option的value值，后面为html里面的值
                                     initial=1,  # 默认选中第二个option
                                     widget=forms.RadioSelect  # 插件表现形式为单选按钮
                                     )
    #标签
    tag = forms.IntegerField(label="教程标签",widget=widgets.RadioSelect(),initial=0)
    articletag = forms.CharField(label="标签", max_length=20,
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
    commitcontent = forms.CharField(label="评论内容", required=True, min_length=10,max_length=500,widget=forms.Textarea(attrs={
                              'id':"commitcontent",'style': 'height: 60px;width:100%;resize:none','placeholder': "评论请大于10字符小于500字符，并且请您的评论遵循国家相关法律法规！",}))