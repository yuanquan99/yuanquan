from django.shortcuts import render_to_response, redirect
from django.contrib import auth

# Create your views here.

def login(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(request, username=username, password=password)
    if user is not None:
        auth.login(request, user)
        return redirect('/')
    else:
        return render_to_response('user/login.html')

def register(request):
    return render_to_response('user/register.html')