from django.shortcuts import render
from article.models import Article
from django.core.paginator import Paginator


def home(request):
    stick_article = Article.objects.filter(is_stick=True)
    articles = Article.objects.filter(is_stick=False)
    if len(articles) > 12:
        articles = articles[:12]
    context = {
        'stick_article': stick_article,
        'articles': articles,
    }
    return render(request, 'index.html', context=context)
