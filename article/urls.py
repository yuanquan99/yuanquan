from django.urls import path
from . import views

urlpatterns = [
    path('<int:article_id>', views.article_detail, name='article_detail'),
    path('add/', views.add_article, name='add_article'),
    path('edit/<int:article_id>', views.edit_article, name='edit_article'),
    path('report', views.report, name='report'),
    path('delete_article', views.delete_article, name='delete_article'),
    path('delete_collection', views.delete_collection, name='delete_collection'),
    path('get_tag_article/<int:tag_id>', views.get_tag_article, name='get_tag_article'),
]
