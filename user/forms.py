from django import forms
from django.contrib import auth
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginForm(forms.Form):
    usercss = {
        'class': 'layui-input',
        'placeholder': '请输入用户名',
    }
    pwdcss = {
        'class': 'layui-input',
        'placeholder': '请输入密码',
    }
    username = forms.CharField(label='用户名', widget=forms.TextInput(attrs=usercss))
    password = forms.CharField(label='密码', widget=forms.PasswordInput(attrs=pwdcss))

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username, password=password)
        if user is None:
            print('user')
            raise forms.ValidationError('用户名或密码不正确')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data


class RegisterFrom(forms.Form):
    usercss = {
        'class': 'layui-input',
        'placeholder': '请输入6-30位用户名',
    }
    mailcss = {
        'class': 'layui-input',
        'placeholder': '请输入您的邮箱',
    }
    pwdcss = {
        'class': 'layui-input',
        'placeholder': '请输入6-30位密码',
    }
    pwdacss = {
        'class': 'layui-input',
        'placeholder': '请输入6-30位密码',
    }
    username = forms.CharField(label='用户名', min_length=6, max_length=30, widget=forms.TextInput(attrs=usercss))
    email = forms.EmailField(label='邮箱', widget=forms.EmailInput(attrs=mailcss))
    password = forms.CharField(label='密码', min_length=6, max_length=30, widget=forms.PasswordInput(attrs=pwdcss))
    password_again = forms.CharField(label='确认密码', min_length=6, max_length=30, widget=forms.PasswordInput(attrs=pwdacss))

    def clean_username(self):
        print('clean_username')
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_password_again(self):
        password = self.cleaned_data['password']
        passord_again = self.cleaned_data['password_again']
        if password != passord_again:
            raise forms.ValidationError('两次输入的密码不一致')
        return password
