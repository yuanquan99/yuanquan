from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='my_home'),
    path('home/<str:user_name>', views.user_home, name='user_home'),
    path('', views.index, name='user_info'),
    path('set/', views.settings, name='settings'),
    path('message/', views.message, name='message'),
    path('all_notifications', views.all_notifications, name='all_notifications'),
    path('collect_change/', views.collect_change, name='collect_change'),
    path('change_user_info/', views.change_user_info, name='change_user_info'),
    path('change_password/', views.change_password, name='change_password'),
]
