from django.contrib import admin

# Register your models here.
from .models import MyUser
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _


@admin.register(MyUser)
class MyUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'mobile', 'qq', 'weChat']
    # 将fieldsets转换为列表，否则无法更改元祖的元素
    fieldsets = list(UserAdmin.fieldsets)
    fieldsets[1] = (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'mobile',
                                                     'qq', 'weChat')})
