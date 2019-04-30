from django.db import models
from django.contrib.auth.models import AbstractUser
from article.views import Article


class User(AbstractUser):
    nickname = models.CharField(max_length=30, default='', verbose_name='昵称', blank=True, null=True)
    phone = models.CharField(max_length=12, default='', verbose_name='手机号', blank=True, null=True)
    city = models.CharField(max_length=20, default='未知', verbose_name='城市', blank=True, null=True)
    desc = models.CharField(max_length=100, default='', verbose_name='签名', blank=True, null=True)
    collect_articles = models.ManyToManyField(Article, blank=True)
    sex = models.IntegerField(default=0, verbose_name='性别', blank=True, null=True)
    url = models.ImageField(default='/static/user_pic/yuanquan4_d5f07dbecd0fe63c048243cf2546b2dc.jpg')
    is_mail_active = models.BooleanField(default=False)

    class Meta(AbstractUser.Meta):
        ordering = ('is_active', 'date_joined')
