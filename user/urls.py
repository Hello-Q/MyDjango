from django.urls import path
from . import views


urlpatterns = [
    # 用户登录
    path('login.html', views.loginView, name='login'),
    # 用户注册
    path('register.html', views.registerView, name='register'),
    # 修改密码
    path('setpassword.html', views.setpasswordView, name='setpassword'),
    # 注销登录
    path('logout.html', views.logoutView, name='logout'),
    # 找回密码
    path('findpassword.html', views.findPassword, name='findPassword')
]
