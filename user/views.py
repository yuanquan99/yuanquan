from django.shortcuts import redirect, render, HttpResponse
from django.contrib import auth
from django.urls import reverse
from .forms import LoginForm, RegisterFrom
from django.contrib.auth import get_user_model
from article.models import Article

User = get_user_model()

# Create your views here.


def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            print('login success!')
            return redirect(request.GET.get('from', reverse('home')))

    login_form = LoginForm()
    context = {
        'login_form': login_form,
    }
    return render(request, 'user/login.html', context=context)


def logout(request):
    auth.logout(request)
    return HttpResponse('您已成功注销')


def register(request):
    if request.method == 'POST':
        reg_form = RegisterFrom(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            password = reg_form.cleaned_data['password']
            email = reg_form.cleaned_data['email']
            user = User.objects.create_user(username, email, password)
            user.save()
            user = auth.authenticate(username=username, password=password)
            return render(request, 'index.html')
    reg_form = RegisterFrom()
    context = {
        'reg_form': reg_form,
    }
    return render(request, 'user/reg.html', context=context)


def home(request):
    context = {

    }
    return render(request, "user/home.html", context=context)


def index(request):
    stick_article = Article.objects.all()
    article = Article.objects.filter(is_stick=False)
    context = {
        'stick_article': stick_article,
        'article': article,
    }
    return render(request, 'user/index.html', context=context)


def settings(request):
    return render(request, 'user/set.html')


def message(request):
    return render(request, 'user/message.html')
