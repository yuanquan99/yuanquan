from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    nickname = models.CharField(max_length=30, default='', verbose_name='昵称', blank=True, null=True)
    phone = models.CharField(max_length=12, default='', verbose_name='手机号', blank=True, null=True)
    city = models.CharField(max_length=20, default='未知', verbose_name='城市', blank=True, null=True)
    desc = models.CharField(max_length=100, default='', verbose_name='签名', blank=True, null=True)
    sex = models.IntegerField(default=0, verbose_name='性别', blank=True, null=True)

    class Meta(AbstractUser.Meta):
        pass