from django.contrib import admin

# Register your models here.
from .models import Article
from .models import ArticleType, ArticleTag


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'author',
        'content',
        'read_num',
        'type',
        'create_time',
        'update_time',
        'is_stick',
        'is_deleted',

    ]
    ordering = ['id'] # 倒序‘-id’


@admin.register(ArticleType)
class TypeAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'type_name',
        'is_delete',
    ]
    ordering = ['id']


@admin.register(ArticleTag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'tag_name', 'is_delete']
    ordering = ['id']
