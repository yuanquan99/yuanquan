# Generated by Django 2.2 on 2019-04-25 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='zan_num',
            field=models.IntegerField(default=0, verbose_name='赞'),
        ),
    ]