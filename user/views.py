from django.shortcuts import render, redirect
from user.models import MyUser as User
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from .form import MyUserCreationForm
from django.contrib.auth.models import Permission
import random


# Create your views here.
def loginView(request):
    # 设置标题和另外两个url链接
    title = '登录'
    unit_2 = '/user/register.html'
    unit_2_name = '立即注册'
    unit_1 = '/user/setpassword.html'
    unit_1_name = '修改密码'
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if User.objects.filter(username=username):
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                return redirect('/')
            else:
                tips = '账号密码错误，请重新输入'
        else:
            tips = '用户不存在，请注册'
    return render(request, 'user.html', locals())


def registerView(request):
    title = '注册'
    unit_2 = '/user/login.html'
    unit_2_name = '立即登录'
    unit_1 = '/user/setpassword'
    unit_1_name = '修改密码'
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if User.objects.filter(username=username):
            tips = '用户名已存在'
        else:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            tips = '注册成功，请登录'
            permission = Permission.objects.get(codename='visit_Product')
            user.user_permissions.add(permission)
            print(user.has_perm('visit_Product'))
    return render(request, 'user.html', locals())


# # 使用表单实现用户注册
# def registerView2(request):
#     if request.method == 'POST':
#         user = MyUserCreationForm(request.POST)
#         if user.is_valid():
#             tips = '注册成功'
#             user = MyUserCreationForm()
#         else:
#             user = MyUserCreationForm()
#     return render(request, 'creation_user.html', locals())

def setpasswordView(request):
    title = '修改密码'
    unit_2 = '/user/login.html'
    unit_2_name = '立即登录'
    unit_1 = '/user/register.html'
    unit_1_name = '立即注册'
    new_password = True
    if request.method == 'POST':
        username = request.POST.get('username', '')
        old_password = request.POST.get('password', '')
        new_password = request.POST.get('new_password', '')
        if User.objects.filter(username=username):
            user = authenticate(username=username, password=old_password)
            if user:
                user.set_password(new_password)
                user.save()
                tips = '密码修改成功'
            else:
                tips = '原密码错误'
        else:
            tips = '用户不存在'
    return render(request, 'user.html', locals())


def logoutView(request):
    logout(request)
    return redirect('/')


# 找回密码
def findPassword(request):
    button = '获取验证码'
    # new_password = False
    if request.method == 'POST':
        username = request.POST.get('username', 'root')
        VerificationCode = request.POST.get('VerificationCode', '')
        password = request.POST.get('password', '')
        user = User.objects.filter(username=username)
        # 用户不存在
        if not user:
            tips = '用户' + username + '不存在'
        else:
            # 判断验证码是否已发送
            if not request.session.get('VerificationCode', ''):
                print(request.session.get('VerificationCode'))
                # 发送验证码并将验证码写入session
                button = '重置密码'
                tips = '验证码已发送'
                new_password = True
                VerificationCode = str(random.randint(1000, 9999))
                request.session['VerificationCode'] = VerificationCode
                user[0].email_user('找回密码', '验证码为'+VerificationCode)
            # 匹配输入的验证码是否正确
            elif VerificationCode == request.session.get('VerificationCode'):
                # 密码加密处理并保存到数据库
                dj_ps = make_password(password, None, 'pbkdf2_sha256')
                user[0].password = dj_ps
                user[0].save()
                del request.session['VerificationCode']
                tips = '密码已重置'
            # 输入验证码错误
            else:
                tips = '验证码错误，请重新获取'
                new_password = False
                del request.session['VerificationCode']
    return render(request, 'user1.html', locals())
