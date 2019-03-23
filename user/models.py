from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    nickname = models.CharField(max_length=30, default='', verbose_name='昵称')
    phone = models.CharField(max_length=12, default='', verbose_name='手机号')

    class Meta(AbstractUser.Meta):
        pass