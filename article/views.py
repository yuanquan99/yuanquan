from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.core.paginator import Paginator
from .models import Article, ArticleType, Report, ArticleTag
from django.contrib.contenttypes.models import ContentType
from read_count.models import ReadNum, ReadDetail
from django.utils import timezone
from read_count.utils import get_hot_article, get_jing_article
from comment.forms import CommentForm, ArticleForm
from django.http import JsonResponse
from django.db.models import ObjectDoesNotExist
import markdown


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
    comments = article.comment_set.filter(display=True)
    hot_articles = get_hot_article()
    comment_form = CommentForm()
    article.content = markdown.markdown(article.content, extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    article.content.replace('\n', '  \n')
    context = {
        'article': article,
        'types': types,
        'comments': comments,
        'hot_articles': hot_articles,
        'comment_form': comment_form,
    }
    response = render(request, 'article/detail.html', context)
    response.set_cookie('article_%s_read' % article_id, 'true', max_age=3600)
    return response


def article_type(request, classify_id):
    if classify_id == 0:
        articles = Article.objects.filter(display=True)
    else:
        classify = ArticleType.objects.get(pk=classify_id)
        articles = Article.objects.filter(type=classify, display=True)

    type_ = request.GET.get('type', '0')
    print(type_, articles)
    if type_ == '1':
        articles = articles.order_by('-last_comment_time')
    elif type_ == '2':
        articles = get_hot_article(type_=1, type=classify_id)
    elif type_ == '3':
        articles = get_jing_article(type=classify_id)

    paginator = Paginator(articles, 12)
    page_articles = paginator.get_page(request.GET.get('page', 1))
    currentr_page_num = page_articles.number # 获取当前页码
    # 获取当前页码前后各2页的页码范围
    page_range = list(range(max(currentr_page_num - 2, 1), currentr_page_num)) + \
                 list(range(currentr_page_num, min(currentr_page_num + 2, paginator.num_pages) + 1))
    # 加上省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    print(page_range)

    types = ArticleType.objects.filter(display=True)
    hot_articles = get_hot_article()
    context = {
        'articles': page_articles,
        'types': types,
        'hot_articles': hot_articles,
        'page_range': page_range,
        'type': type_,
        'classify_id': classify_id,
    }
    return render(request, 'article/index.html', context)


def add_article(request):
    if request.method == 'POST':
        print(request.POST)
        title = request.POST.get('title', '')
        type_name = request.POST.get('type', '')
        # 帖子内容, markdown以两个空格为换行符
        content = request.POST.get('content', '')
        content_split = content.split('\r\n')
        content = ''
        for item in content_split:
            if item.endswith('  '):
                content = content + item + '\r\n'
            else:
                content = content + item + '  \r\n'
        tags = request.POST.get('tags', '').split(';')
        print(tags)
        if type_name != '' and type_name is not None:
            type_name = ArticleType.objects.get(type_name=type_name)
            article = Article(title=title, author=request.user, content=content, type=type_name)
            article.save()
            for tag in tags:
                tag = tag.rstrip()
                if tag == '':
                    continue
                print('tag=', tag)
                tag_, created = ArticleTag.objects.get_or_create(tag_name=tag)
                article.tags.add(tag_)
            article.save()

            return redirect('/article/%d' % article.pk)

    article_from = ArticleForm()
    types = ArticleType.objects.filter(display=True, for_super_user=False)
    admin_types = ArticleType.objects.filter(display=True, for_super_user=True)
    context = {
        'types': types,
        'admin_types': admin_types,
        'article_from': article_from,
    }
    return render(request, 'article/add.html', context=context)


def edit_article(request, article_id):
    article = Article.objects.get(id=article_id)
    if request.method == 'POST':
        title = request.POST.get('title', '')
        type_name = request.POST.get('type', '')
        content = request.POST.get('content', '')
        content_split = content.split('\r\n')
        content = ''
        for item in content_split:
            if item.endswith('  '):
                content = content + item + '\r\n'
            else:
                content = content + item + '  \r\n'
        tags = request.POST.get('tags', '').split(';')
        if type_name != '' and type_name is not None:
            type_name = ArticleType.objects.get(type_name=type_name)
            article.title = title; article.content = content; article.type = type_name
            article.save()
            article.tags.clear()
            for tag in tags:
                tag = tag.rstrip()
                if tag == '':
                    continue
                print('tag=', tag)
                tag_, created = ArticleTag.objects.get_or_create(tag_name=tag)
                article.tags.add(tag_)
            article.save()
            return redirect('/article/%d' % article.pk)

    types = ArticleType.objects.filter(display=True)
    admin_types = ArticleType.objects.filter(display=True, for_super_user=True)
    article_from = ArticleForm()
    context = {
        'types': types,
        'admin_types': admin_types,
        'article': article,
        'article_from': article_from,
        'edit': 1,
    }
    return render(request, 'article/add.html', context=context)


def report(request):
    data = {
        'status': 'ERROR',
        'message': '未知错误, 请稍后重试',
    }
    if request.method != 'POST':
        return JsonResponse(data)
    if request.user is None:
        data['message'] = '您尚未登录, 请先登录'
        return JsonResponse(data)
    try:
        article = Article.objects.get(pk=request.POST.get('article_id', -1))
    except ObjectDoesNotExist:
        data['message'] = '您举报的帖子不存在, 请刷新后重试'
        return JsonResponse(data)
    report, created = Report.objects.get_or_create(article = article, author=request.user)
    if not created:
        print('asdad')
        data['message'] = '您已举报过该帖子, 我们会尽快处理'
        return JsonResponse(data)
    report.liyou = request.POST.get('liyou', 'ERROR, 未获取到举报理由')
    data['status'] = 'SUCCESS'
    return JsonResponse(data)


def delete_article(request):
    data = {
        'status': 'ERROR',
        'message': '未知错误, 请稍后重试',
    }
    if request.method != 'POST':
        return JsonResponse(data)
    if request.user is None:
        data['message'] = '您尚未登录, 请先登录'
        return JsonResponse(data)
    try:
        article = Article.objects.get(pk=request.POST.get('article_id', -1))
    except ObjectDoesNotExist:
        data['status'] = 'SUCCESS'
        return JsonResponse(data)
    article.display = False
    article.save()
    data['status'] = 'SUCCESS'
    return JsonResponse(data)


def delete_collection(request):
    data = {
        'status': 'ERROR',
        'message': '未知错误, 请稍后重试',
    }
    if request.method != 'POST':
        return JsonResponse(data)
    if request.user is None:
        data['message'] = '您尚未登录, 请先登录'
        return JsonResponse(data)
    try:
        article = Article.objects.get(pk=request.POST.get('article_id', -1))
    except ObjectDoesNotExist:
        data['status'] = 'SUCCESS'
        return JsonResponse(data)
    request.user.collect_articles.remove(article)
    data['status'] = 'SUCCESS'
    return JsonResponse(data)


def get_tag_article(request, tag_id):
    try:
        tag = ArticleTag.objects.get(pk=tag_id)
    except ObjectDoesNotExist:
        pass
