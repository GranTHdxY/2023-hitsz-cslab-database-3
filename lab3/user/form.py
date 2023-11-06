from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128)
    password = forms.CharField(label="密码", max_length=256)

class SignupForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128)
    password1 = forms.CharField(label="密码",)
    password2 = forms.CharField(label="确认密码")
    tel = forms.CharField(label = "电话号码", max_length=12)
    role_choices = (
        ('1', '顾客'),
        ('2', '商家'),
        ('3', '食堂管理员'),
    )
    usertype = forms.ChoiceField(label="选择用户类型", choices=role_choices)