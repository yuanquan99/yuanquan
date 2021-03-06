# Generated by Django 2.2 on 2019-04-29 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('read_count', '0003_readdetail_comment_num'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='readdetail',
            options={'ordering': ['hot_num']},
        ),
        migrations.AlterModelOptions(
            name='readnum',
            options={'ordering': ['read_num']},
        ),
        migrations.AddField(
            model_name='readdetail',
            name='hot_num',
            field=models.IntegerField(default=0, verbose_name='热读'),
        ),
    ]
