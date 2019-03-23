from django.shortcuts import redirect, render, render_to_response
from django.contrib import auth
from .forms import LoginForm, RegisterFrom
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.


def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return credits('home')

    login_form = LoginForm()
    context = {
        'login_form': login_form,
    }
    return render(request, 'user/login.html', context=context)


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
            return redirect('home')
    reg_form = RegisterFrom()
    context = {
        'reg_form': reg_form,
    }
    return render(request, 'user/reg.html', context=context)


def home(request):
    return render_to_response("user/home.html")


def index(request):
    return render_to_response('user/index.html')


def settings(request):
    return render_to_response('user/set.html')


def message(request):
    return render_to_response('user/message.html')
