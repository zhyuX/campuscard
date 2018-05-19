from django import forms


# 登录表单验证
class LoginForm(forms.Form):
    # 用户名密码不能为空
    account = forms.CharField(required=True)
    password = forms.CharField(required=True)