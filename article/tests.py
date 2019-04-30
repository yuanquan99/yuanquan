from django.test import TestCase
from .models import Article
from django.db.models import Sum, Count, IntegerField

# Create your tests here.

articles = Article.objects.annotate(sum=('comment_num') + ('read_num')).order_by(sum)
articles.order_by()