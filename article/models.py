from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings


class ArticleType(models.Model):
    type_name = models.CharField(max_length=30, verbose_name='类型')
    is_delete = models.BooleanField(default=False, verbose_name='是否显示')

    def __str__(self):
        return self.type_name


class ArticleTag(models.Model):
    tag_name = models.CharField(max_length=30, verbose_name='标签')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    def __str__(self):
        return self.tag_name


class Article(models.Model):
    title = models.CharField(max_length=100, verbose_name='题目')
    content = models.TextField(verbose_name='内容')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, default=1, verbose_name='作者')
    # 默认与User 里 pk=1的用户关联
    tags = models.ManyToManyField(ArticleTag, blank=True, verbose_name='标签')
    # 允许为空
    type = models.ForeignKey(ArticleType, on_delete=models.DO_NOTHING, default=1, verbose_name='类型')
    read_num = models.IntegerField(default=0, verbose_name='阅读数')
    comment_num = models.IntegerField(default=0, verbose_name='评论数')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='最近更新')
    is_deleted = models.BooleanField(default=False, verbose_name='是否删除')
    is_stick = models.BooleanField(default=False, verbose_name='是否置顶')

    def __str__(self):
        return '%s' % self.title

    class Meta:
        ordering = ['-create_time']


# class Comment(models.Model):
#     content = models.TextField(verbose_name='评论内容')
#     author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, verbose_name='评论者')
#     create_time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
#     is_delete = models.BooleanField(default=False, blank=False, null=False, verbose_name='是否显示')
#
#     class Meta:
#         ordering = ['-create_time']
#         verbose_name = '评论'
#
#     def __str__(self):
#         return self.content
