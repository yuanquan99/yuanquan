from django.shortcuts import redirect, render, HttpResponse
from django.contrib import auth
from django.urls import reverse
from .forms import LoginForm, RegisterFrom
from django.contrib.auth import get_user_model
from article.models import Article
from django.db.models import ObjectDoesNotExist
from django.http import JsonResponse

User = get_user_model()


def login(request):
    login_form = LoginForm()
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))

    context = {
        'login_form': login_form,
    }
    return render(request, 'user/login1.html', context=context)


def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('home')))


def register(request):
    reg_form = RegisterFrom()
    if request.method == 'POST':
        reg_form = RegisterFrom(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            password = reg_form.cleaned_data['password']
            email = reg_form.cleaned_data['email']
            user = User.objects.create_user(username, email, password)
            user.save()
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect(request.GET.get('from', reverse('home')))

    context = {
        'reg_form': reg_form,
    }
    return render(request, 'user/reg.html', context=context)


def home(request):
    articles = Article.objects.filter(author=request.user)
    context = {
        'articles': articles,
    }
    return render(request, "user/home.html", context=context)


def user_home(request, user_name):
    try:
        user = User.objects.get(username=user_name)
    except ObjectDoesNotExist:
        return render(request, '404.html')
    articles = Article.objects.filter(author=user)
    context = {
        'query_user': user,
        'articles': articles,
    }
    return render(request, "user/user_home.html", context=context)


def index(request):
    col = request.GET.get('col', '0')
    col = int(col)
    articles = Article.objects.filter(display=True, author=request.user)
    collect_articles = request.user.collect_articles.all()
    context = {
        'articles': articles,
        'collect_articles': collect_articles,
        'col': col,
    }
    return render(request, 'user/index.html', context=context)


def settings(request):
    return render(request, 'user/set.html')


def message(request):
    return render(request, 'user/message.html')


def all_notifications(request):
    return render(request, 'user/message.html')


def collect_change(request):
    data = {
        'status': 'ERROR',
    }
    if not request.user:
        data['message'] = '尚未登录, 请登陆后重试'
        return JsonResponse(data)
    if request.method == 'POST':
        article_id = request.POST.get('article_id')
        try:
            article = Article.objects.get(pk=article_id)
        except ObjectDoesNotExist:
            data['message'] = '您收藏的帖子不存在'
            return JsonResponse(data)

        if request.POST.get('is_like') == 'true':
            if request.user.collect_articles.filter(pk=article_id):
                data['message'] = '以收藏过这篇帖子'
                return JsonResponse(data)
            request.user.collect_articles.add(article)
        else:
            if not request.user.collect_articles.filter(pk=article_id):
                data['message'] = '您还未收藏过这篇帖子'
                return JsonResponse(data)
            request.user.collect_articles.remove(article)
        data['collect_num'] = article.user_set.count()
        data['status'] = 'SUCCESS'
    return JsonResponse(data)


def change_user_info(request):
    data = {
        'status': 'ERROR',
        'message': 'ERROR, 请稍后重试',
    }
    if request.user is None:
        data['message'] = '未登录, 请登陆后继续操作'
        return JsonResponse(data)

    if request.method == 'POST':
        email = request.POST.get('email', '')
        nickname = request.POST.get('nickname', '')
        sex = request.POST.get('sex', '0')
        city = request.POST.get('city', '未知')
        sign = request.POST.get('sign', '')
        if email != '' and email != request.user.email:
            request.user.email = email
            request.user.is_mail_active = False
            data['is_mail_change'] = True
        if nickname != '' and nickname != request.user.nickname:
            request.user.nickname = nickname
        if sex == '1':
            sex = 1
        else:
            sex = 0
        if sex != request.user.sex:
            request.user.sex = sex
        if city != '未知' and city != request.user.city:
            request.user.city = city
        if sign != '' and sign != request.user.desc:
            request.user.desc = sign
        request.user.save()
        data['status'] = 'SUCCESS'

    return JsonResponse(data)


def change_password(request):
    data = {
        'status': 'ERROR',
        'message': 'ERROR, 请稍后重试',
    }
    if request.user is None:
        data['message'] = '未登录, 请登陆后继续操作'
        return JsonResponse(data)

    if request.method == 'POST':
        now_password = request.POST.get('now_password', '')
        new_password = request.POST.get('new_password', '')
        re_password = request.POST.get('re_password', '')
        print(now_password, new_password, re_password)
        user = auth.authenticate(username=request.user.username, password=now_password)
        print(user)
        if user is None:
            data['message'] = '密码错误'
            return JsonResponse(data)
        if len(new_password) < 6 or len(new_password) > 16:
            data['message'] = '密码长度不合法'
            return JsonResponse(data)
        if new_password != re_password:
            data['message'] = '两次输入的密码不一致'
            return JsonResponse(data)
        request.user.set_password(new_password)
        request.user.save()
    auth.logout(request)
    data['status'] = 'SUCCESS'
    return JsonResponse(data)
