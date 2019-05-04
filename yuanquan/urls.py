"""yuanquan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import home
import user, article, comment
from django.conf import settings
from django.conf.urls.static import static
import notifications.urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home.home, name='home'),
    path('article/', include('article.urls')),
    path('user/', include('user.urls')),
    path('like/', include('comment.urls')),
    path('login/', user.views.login, name='login'),
    path('logout/', user.views.logout, name='logout'),
    path('register/', user.views.register, name='register'),
    path('error404/', home.error404, name='error404'),
    path('search/', home.search, name='search'),
    path('test/', home.test, name='test'),
    path('classify/<int:classify_id>', article.views.article_type, name='classify_type'),
    path('add_comment/<int:article_id>', comment.views.add_comment, name='add_comment'),
    path('info/', home.info, name='info'),
    path('record/', home.record, name='record'),
    path('load_file/', home.load_file, name='load_file'),
    path('notifications/', include(notifications.urls, namespace='notifications')),
    path('delete_all_notification', home.delete_all_notification, name='delete_all_notification'),
    path('delete_notification', home.delete_notification, name='delete_notification'),
    path('mdeditor/', include('mdeditor.urls')),

] + static('/pic', document_root=settings.MEDIA_ROOT)

