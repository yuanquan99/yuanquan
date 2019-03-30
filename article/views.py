from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Article, ArticleType
# Create your views here.


def article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    context = {
        'article': article,
    }
    return render(request, 'article/detail.html', context)


def article_list(request):
    articles = Article.objects.filter(is_deleted=False)
    context = {
        'articles': articles,
    }
    return render(request, 'article/index.html', context)


def article_type(request, article_type_id):
    type = get_object_or_404(ArticleType, pk=article_type_id)
    articles = Article.objects.filter(type=type, is_deleted=False)
    context = {
        'articles': articles,
    }
    return render(request, 'article/article_type.html', context)


def add_article(request):
    return render(request, 'article/add.html')
