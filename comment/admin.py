from django.contrib import admin
from .models import Comment, LikeCount


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'article', 'content', 'author', 'create_time', 'display', ]
    ordering = ['id']  # 倒序‘-id’


@admin.register(LikeCount)
class LickCountAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_like_object', 'object_id', 'like_num']
    ordering = ['id']
