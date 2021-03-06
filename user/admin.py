from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext, gettext_lazy as _
from .models import Info

User = get_user_model()


@admin.register(Info)
class InfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(User)
class UserAdmins(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('nickname', 'phone', 'email', 'city', 'sex', 'info')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    list_display = ('username', 'email', 'phone', 'nickname', 'city', 'url', 'is_staff', 'is_active', 'is_superuser')
