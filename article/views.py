from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse, Http404
from .models import Article, ArticleType
# Create your views here.

def article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    context = {
        'article': article,
    }
    return render_to_response('article/article.html', context)
    # return render(request, 'article.html', content)


def article_list(request):
    articles = Article.objects.filter(is_deleted=False)
    context = {
        'articles': articles,
    }
    return render_to_response('article/article_list.html', context)

def article_type(request, article_type_id):
    type = get_object_or_404(ArticleType, pk=article_type_id)
    articles = Article.objects.filter(type=type, is_deleted=False)
    context = {
        'articles': articles,
    }
    return render_to_response('article/article_type.html', context)