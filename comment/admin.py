from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'article', 'author', 'create_time', 'display', ]
    ordering = ['id']  # 倒序‘-id’
