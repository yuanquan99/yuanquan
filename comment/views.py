from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, get_object_or_404
from article.models import Article
from django.http import JsonResponse
from django.db.models import ObjectDoesNotExist
from .models import Comment, LikeCount, LikeRecord
from read_count.models import ReadDetail
from django.utils import timezone


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
        comment.save() # 保存评论
        article.last_comment_time = timezone.now()
        article.save() # 修改article的最近评论时间
        data['status'] = 'SUCCESS'
        data['user'] = request.user.username
        data['is_superuser'] = comment.author.is_superuser
        data['is_louzhu'] = comment.author == article.author
        data['comment_time'] = comment.create_time.timestamp()
        data['comment_content'] = comment.content
        ct = ContentType.objects.get_for_model(Article)
        readdetail, created = ReadDetail.objects.get_or_create(content_type=ct, object_id=article_id, data=timezone.now().date())
        readdetail.comment_num += 1
        readdetail.save() # 热度统计相关
    return JsonResponse(data)


def ErrorResponse(code, message):
    data = {
        '': 'ERROR',
        'code': code,
        'message': message
    }
    return JsonResponse(data)


def SuccessResponse(like_num):
    data = {
        'status': 'SUCCESS',
        'like_num': like_num,
    }
    return JsonResponse(data)


def like_change(request):
    # 获取数据
    user = request.user
    if not user.is_authenticated:
        return ErrorResponse(400, 'you were not login')

    content_type = request.GET.get('content_type')
    object_id = int(request.GET.get('object_id'))

    try:
        content_type = ContentType.objects.get(model=content_type)
        model_class = content_type.model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except ObjectDoesNotExist:
        return ErrorResponse(401, 'object not exist')

    # 处理数据
    if request.GET.get('is_like') == 'true':
        # 要点赞
        like_record, created = LikeRecord.objects.get_or_create(content_type=content_type, object_id=object_id, user=user)
        if created:
            # 未点赞过，进行点赞
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            like_count.like_num += 1
            like_count.save()
            return SuccessResponse(like_count.like_num)
        else:
            # 已点赞过，不能重复点赞
            return ErrorResponse(402, 'you were liked')
    else:
        # 要取消点赞
        if LikeRecord.objects.filter(content_type=content_type, object_id=object_id, user=user).exists():
            # 有点赞过，取消点赞
            like_record = LikeRecord.objects.get(content_type=content_type, object_id=object_id, user=user)
            like_record.delete()
            # 点赞总数减1
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            if not created:
                if like_count.like_num > 0:
                    like_count.like_num -= 1
                like_count.save()
                return SuccessResponse(like_count.like_num)
            else:
                return ErrorResponse(404, 'data error')
        else:
            # 没有点赞过，不能取消
            return ErrorResponse(403, 'you were not liked')
