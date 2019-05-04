from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from article.models import Article, ArticleType
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.conf import settings
from read_count.utils import get_hot_article
from notifications.models import Notification


def home(request):
    stick_article = Article.objects.filter(is_stick=True)
    articles = Article.objects.filter(is_stick=False, display=True)[:12]
    hot_articles = get_hot_article()
    types = ArticleType.objects.filter(display=True)
    context = {
        'stick_article': stick_article,
        'articles': articles,
        'types': types,
        'hot_articles': hot_articles,
    }
    return render(request, 'index.html', context=context)


def search(request):
    key_word = request.GET.get('q', '').rstrip()
    key_word = key_word.split(' ')
    filter_word = None
    for word in key_word:
        if filter_word:
            filter_word = filter_word | Q(title__contains=word)
        else:
            filter_word = Q(title__contains=word)
    key_blog = []
    if filter_word:
        key_blog = Article.objects.filter(filter_word)

    page = Paginator(key_blog, 12)
    articles = page.get_page(request.GET.get('page', 1))

    if len(key_word) == 1:
        key_word = key_word[0]
    hot_articles = get_hot_article()
    types = ArticleType.objects.filter(display=True)
    context = {
        "key_word": key_word,
        "article_num": len(articles),
        "articles": articles,
        'hot_articles': hot_articles,
        'types': types,
    }
    return render(request, "search.html", context=context)


def test(request):
    from comment.forms import CommentForm
    commonform = CommentForm()
    return render(request, 'user/activate.html', context={'commonform': commonform})


def info(request):
    return render(request, 'hnust_acm.html')


def record(request):
    return render(request, 'record.html')


def error404(request):
    return render(request, '404.html')


def load_file(request):
    print(request.POST.get('result', ''))
    print(request.POST)
    f1 = request.FILES['picture']
    pic_path = settings.MEDIA_ROOT + request.user.username + '_' + f1.name
    print(pic_path)
    user = request.user
    user.url = '/static/user_pic/' + request.user.username + '_' + f1.name
    user.save()
    print(request.user.url)
    with open(pic_path, 'wb') as pic:
        for c in f1.chunks():
            pic.write(c)

    data = {
        'url': '/static/user_pic/' + request.user.username + '_' + f1.name,
    }
    return JsonResponse(data)


def delete_all_notification(request):
    notifications = request.user.notifications.read()
    notifications.delete()
    return redirect(reverse('all_notifications'))


def delete_notification(request):
    notification_id = request.GET.get('notification_id', '')
    notification = get_object_or_404(Notification, recipient=request.user, id=notification_id)
    print(notification)
    notification.delete()
    data = {
        'status': 'SUCCESS'
    }
    return JsonResponse(data)
