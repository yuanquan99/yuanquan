from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Article, ArticleType


def article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    context = {
        'article': article,
    }
    return render(request, 'article/detail.html', context)


def article_list(request):
    articles = Article.objects.filter(is_deleted=False)
    paginate = Paginator(articles, 12)
    page_articles = paginate.get_page(request.GET.get('page', 1))

    context = {
        'articles': page_articles,
    }
    return render(request, 'article/index.html', context)


def article_type(request, classify_id):
    classify = get_object_or_404(ArticleType, pk=classify_id)
    articles = Article.objects.filter(type=classify, is_deleted=False)
    context = {
        'articles': articles,
    }
    return render(request, 'article/index.html', context)


def add_article(request):
    return render(request, 'article/add.html')

