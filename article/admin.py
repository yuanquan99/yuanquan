from django.contrib import admin
from .models import Article
from .models import ArticleType, ArticleTag, Report


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'author',
        'read_num',
        'type',
        'create_time',
        'last_comment_time',
        'is_stick',
        'display',
        'get_read_num'
    ]
    ordering = ['id'] # 倒序‘-id’


@admin.register(ArticleType)
class TypeAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'type_name',
        'display',
    ]
    ordering = ['id']


@admin.register(ArticleTag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'tag_name', 'display']
    ordering = ['id']


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['author', 'article', 'article_pk', 'liyou']


admin.site.site_header = "HNUST ACM社区后台管理"
