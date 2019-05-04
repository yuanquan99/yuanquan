from django import template
from django.contrib.auth.decorators import login_required
register = template.Library()


@register.simple_tag
def get_coll_num(article):
    return '%d' % article.user_set.count()


@register.simple_tag
def get_collect_class(article, now_user):
    if now_user.collect_articles.filter(pk=article.pk):
        return 'active'
    return ''


@register.simple_tag
def get_collect_title(article, now_user):
    if now_user.collect_articles.filter(pk=article.pk):
        return '取消收藏'
    return '收藏'
