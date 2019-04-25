from django.shortcuts import render, get_object_or_404
from article.models import Article
from django.http import JsonResponse
from django.db.models import ObjectDoesNotExist
from .models import Comment
import time


def add_comment(request, article_id):
    data = {}
    if request.method == 'POST':
        try:
            article = Article.objects.get(pk=article_id)
        except ObjectDoesNotExist:
            data['status'] = 'FAIL'
            data['error'] = '评论的对象不存在'
            return JsonResponse(data)
        content = request.POST.get('detail-comment', '')
        author = request.user

        if author is None:
            data['status'] = 'FAIL'
            data['error'] = '您尚未登录, 请登录后评论'
            return JsonResponse(data)
        comment = Comment(content=content, article=article, author=author)
        comment.save()
        data['status'] = 'SUCCESS'
        data['user'] = request.user.username
        data['is_superuser'] = comment.author.is_superuser
        data['is_louzhu'] = comment.author == article.author
        data['comment_time'] = comment.create_time.timestamp()
        data['comment_content'] = comment.content
        return JsonResponse(data)
