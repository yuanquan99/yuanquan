from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.conf import settings
from read_count.models import ReadNum
from django.db.models import ObjectDoesNotExist
from django.utils import timezone


class ArticleType(models.Model):
    type_name = models.CharField(max_length=30, verbose_name='类型')
    display = models.BooleanField(default=True, verbose_name='是否显示')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.type_name


class ArticleTag(models.Model):
    tag_name = models.CharField(max_length=30, verbose_name='标签')
    display = models.BooleanField(default=True, verbose_name='是否显示')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

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
    last_comment_time = models.DateTimeField(default=timezone.now, verbose_name='最近评论时间')
    display = models.BooleanField(default=True, verbose_name='是否显示')
    is_stick = models.BooleanField(default=False, verbose_name='是否置顶')

    def __str__(self):
        return '%s' % self.title

    def get_read_num(self):
        try:
            ct = ContentType.objects.get_for_model(Article)
            Readnum = ReadNum.objects.get(content_type=ct, object_id=self.pk)
            return Readnum.read_num
        except ObjectDoesNotExist:
            return 0

    class Meta:
        ordering = ['-create_time']
        verbose_name = '帖子'
        verbose_name_plural = verbose_name

