from django import forms


# 登录表单验证
class LoginForm(forms.Form):
    # 用户名密码不能为空
    account = forms.CharField(required=True)
    password = forms.CharField(required=True)


# 修改密码表单验证
class UpdatePasswordForm(forms.Form):
    old_password = forms.CharField(required=True)
    new_password = forms.CharField(required=True)
    confirm_password = forms.CharField(required=True)