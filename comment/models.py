from django.db import models
from article.models import Article
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Comment(models.Model):
    content = models.TextField(verbose_name='评论内容')
    article = models.ForeignKey(Article, on_delete=models.DO_NOTHING, verbose_name='文章')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, default=1, verbose_name='作者')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    display = models.BooleanField(default=True, verbose_name='是否显示')

    def __str__(self):
        return self.author.username + "'s comment for article[" + self.article.title + "]: " + self.content[:20]

    def get_user(self):
        return self.author

    class Meta:
        ordering = ["-create_time"]
        verbose_name = '评论'
        verbose_name_plural = verbose_name


class LikeCount(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    like_num = models.IntegerField(default=0, verbose_name='赞')


class LikeRecord(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='用户')
    liked_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
