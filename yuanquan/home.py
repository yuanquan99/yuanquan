from django.shortcuts import render
from article.models import Article, ArticleType
from django.core.paginator import Paginator
from django.db.models import Q


def home(request):
    stick_article = Article.objects.filter(is_stick=True)
    articles = Article.objects.filter(is_stick=False)[:12]
    classify = ArticleType.objects.all()[0]
    context = {
        'stick_article': stick_article,
        'articles': articles,
        'classify': classify,
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
    context = {
        "key_word": key_word,
        "article_num": len(articles),
        "articles": articles
    }
    return render(request, "search.html", context=context)


def test(request):
    return render(request, 'test.html')
