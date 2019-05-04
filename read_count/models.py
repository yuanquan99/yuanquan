from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone


class ReadNum(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    read_num = models.IntegerField(default=0, verbose_name='阅读数量')

    class Meta:
        ordering = ['-read_num']
        verbose_name = '阅读数量'
        verbose_name_plural = verbose_name


class ReadDetail(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    data = models.DateField(default=timezone.now, verbose_name='日期')
    read_num = models.IntegerField(default=0, verbose_name='阅读数量')
    comment_num = models.IntegerField(default=0, verbose_name='评论数量')
    hot_num = models.IntegerField(default=0, verbose_name='热度')

    def __str__(self):
        return '%s_%s_%s' % (self.content_object, self.data, self.read_num)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None, *args, **kwargs):
        self.hot_num = self.read_num + self.comment_num * 10
        super(ReadDetail, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-data']
        verbose_name = '阅读数量(按日期分)'
        verbose_name_plural = verbose_name

