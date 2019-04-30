from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.core.paginator import Paginator
from .models import Article, ArticleType
from django.contrib.contenttypes.models import ContentType
from read_count.models import ReadNum, ReadDetail
from django.utils import timezone
from read_count.utils import get_hot_article


def article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if not request.COOKIES.get('article_%s_read' % article_id):
        ct = ContentType.objects.get_for_model(Article)
        readnum, created = ReadNum.objects.get_or_create(content_type=ct, object_id=article_id)
        readnum.read_num += 1
        readnum.save()
        readdetail, created = ReadDetail.objects.get_or_create(content_type=ct, object_id=article_id, data=timezone.now().date())
        readdetail.read_num += 1
        readdetail.save()

    types = ArticleType.objects.filter(display=True)
    comments = article.comment_set.all()
    hot_articles = get_hot_article()
    context = {
        'article': article,
        'types': types,
        'comments': comments,
        'hot_articles': hot_articles,
    }
    response = render(request, 'article/detail.html', context)
    response.set_cookie('article_%s_read' % article_id, 'true', max_age=3600)
    return response


def article_list(request):
    articles = Article.objects.filter(display=True)
    paginate = Paginator(articles, 12)
    page_articles = paginate.get_page(request.GET.get('page', 1))
    types = ArticleType.objects.filter(display=True)
    context = {
        'articles': page_articles,
        'types': types,
    }
    return render(request, 'article/index.html', context)


def article_type(request, classify_id):
    if classify_id == 0:
        articles = Article.objects.filter(display=True)
    else:
        classify = get_object_or_404(ArticleType, pk=classify_id)
        articles = Article.objects.filter(type=classify, display=True)
    types = ArticleType.objects.filter(display=True)
    hot_articles = get_hot_article()
    context = {
        'articles': articles,
        'types': types,
        'hot_articles': hot_articles,
    }
    return render(request, 'article/index.html', context)


def add_article(request):
    if request.method == 'POST':
        title = request.POST.get('title', '')
        type_name = request.POST.get('type', '')
        content = request.POST.get('content', '')
        print(title, type_name, content)
        if type_name != '' and type_name is not None:
            type_name = ArticleType.objects.get(type_name=type_name)
            article = Article(title=title, author=request.user, content=content, type=type_name)
            article.save()
            return redirect('/article/%d' % article.pk)

    types = ArticleType.objects.filter(display=True)
    context = {
        'types': types,
    }
    return render(request, 'article/add.html', context=context)


def edit_article(request, article_id):
    article = Article.objects.get(id=article_id)
    if request.method == 'POST':
        title = request.POST.get('title', '')
        type_name = request.POST.get('type', '')
        content = request.POST.get('content', '')
        print(title, type_name, content)
        if type_name != '' and type_name is not None:
            type_name = ArticleType.objects.get(type_name=type_name)
            article.title = title; article.content = content; article.type = type_name
            article.save()
            return redirect('/article/%d' % article.pk)

    types = ArticleType.objects.filter(display=True)

    context = {
        'types': types,
        'article': article,
    }
    return render(request, 'article/add.html', context=context)
