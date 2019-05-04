from django.db.models import Sum, Q, Count
from .models import ReadDetail
from django.utils import timezone
from article.models import Article
from django.contrib.contenttypes.models import ContentType
import datetime


def get_hot_article(type_=0, type=0):
    today = timezone.now().date()
    search_ = Q(data=today)
    for i in range(1, 4):
        search_ = search_ | Q(data=today - datetime.timedelta(days=i))
    ct = ContentType.objects.get_for_model(Article)
    readdetail = ReadDetail.objects.filter(search_).filter(content_type=ct)
    hot_article = readdetail.values('object_id').annotate(hot_nums=Sum('hot_num')).order_by('-hot_nums')
    if type_ == 0:
        hot_article = hot_article[:12]
    articles = []
    for art in hot_article:
        try:
            article = Article.objects.get(pk=art['object_id'])
            if type == 0 or article.type.pk == type:
                articles.append(article)
        except Exception:
            pass
    return articles


def get_jing_article(type=0):
    today = timezone.now().date()
    search_ = Q(data=today)
    for i in range(1, 4):
        search_ = search_ | Q(data=today - datetime.timedelta(days=i))
    ct = ContentType.objects.get_for_model(Article)
    readdetail = ReadDetail.objects.filter(search_).filter(content_type=ct)
    jing_article = readdetail.values('object_id').annotate(jing_nums=Sum('comment_num')).order_by('-jing_nums')
    articles = []
    for art in jing_article:
        try:
            article = Article.objects.get(pk=art['object_id'])
            if type == 0 or article.type.pk == type:
                articles.append(article)
        except Exception:
            pass
    return articles