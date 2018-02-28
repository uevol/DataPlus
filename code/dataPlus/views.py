#coding=utf-8

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

def login(request):
    """ user login """
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return render(request, 'login/login.html')
    else:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return redirect('/')
            else:
                msg = '用户未激活'
                return render(request, 'login/login.html', locals())
        else:
            msg = '用户名或密码错误'
            return render(request, 'login/login.html', locals())

@login_required
def logout(request):
    """ user logout """
    username = request.user.username
    auth_logout(request)
    return render(request, 'login/login.html', locals())

@login_required
def base(request):
    return render(request, 'base/index.html')
