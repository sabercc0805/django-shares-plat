from django import forms
from captcha.fields import CaptchaField


class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=48, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='验证码')

class UserInfoForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}))
    registertime = forms.CharField(label="注册时间", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}))
    endtime = forms.CharField(label="会员到期时间", max_length=128,
                                   widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    level = forms.CharField(label="会员级别", max_length=128,
                                   widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    phonenum = forms.CharField(label="手机号", max_length=11,min_length=11,widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label="Email",widget=forms.TextInput(attrs={'class': 'form-control'}))


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
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=48, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=48,widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    phonenumber = forms.CharField(label="电话", min_length=11,max_length=11, widget=forms.TextInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='验证码')

class ArticleForm(forms.Form):
    articletitle = forms.CharField(label="文章标题",required = True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    articlecontent = forms.CharField(label="文章内容",required = True, widget=forms.Textarea(attrs={'class': 'form-control'}))