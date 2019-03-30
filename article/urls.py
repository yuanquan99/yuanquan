from django.urls import path
from . import views

urlpatterns = [
    path('', views.article_list, name='article_list'),
    path('<int:article_id>', views.article_detail, name='article_detail'),
    path('type/<int:article_type_id>', views.article_type, name='article_type'),
    path('add/', views.add_article, name='add_article'),
]
