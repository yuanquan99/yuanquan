from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name='user_home'),
    path('', views.index, name='user_info'),
    path('set', views.settings, name='settings'),
    path('message', views.message, name='message'),
]
