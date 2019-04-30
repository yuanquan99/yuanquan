from django.db.models import Sum, Q, Count
from .models import ReadDetail
from django.utils import timezone
from article.models import Article
from django.contrib.contenttypes.models import ContentType
import datetime


def get_hot_article():
    today = timezone.now().date()
    search_ = Q(data=today)
    for i in range(1, 4):
        search_ = search_ | Q(data=today - datetime.timedelta(days=i))
    ct = ContentType.objects.get_for_model(Article)
    readdetail = ReadDetail.objects.filter(search_).filter(content_type=ct)
    hot_article = readdetail.values('object_id').annotate(hot_nums=Sum('hot_num')).order_by('-hot_nums')
    hot_article[:12]
    articles = []
    for art in hot_article:
        articles.append(Article.objects.get(pk=art['object_id']))
    return articles
