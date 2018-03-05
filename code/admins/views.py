# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from utils.paginator import my_paginator
from django.db.models import Q
import datetime
import random, string
from django.contrib.auth import authenticate

import pprint
# Create your views here.

def index(request):
    return render(request, 'index.html', locals())

def MenuList(request):
    return render(request, 'menu/list.html', locals())

def MenuListAPI(request):
    menus = Menu.objects.all()

    # 构造返回数据
    data = [{'id': menu.id, 'name': menu.name, 'code':menu.code, 'url': menu.url, 'comment': menu.comment} for menu in menus]
   
    # 分页处理
    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 10)
    count, data = my_paginator(data, page, limit)

    res = {'code': 0, 'msg': '', 'count': count, 'data': data}
    return JsonResponse(res)

def MenuAdd(request):
    if request.method == 'POST':
        try:
            post_data = {key: value for key, value in request.POST.items() if value and key != 'csrfmiddlewaretoken'}
            Menu(**post_data).save()
            res = {'code': 1, 'msg': '模块已添加！'}
        except Exception as e:
            res = {'code': 0, 'msg': str(e)}
        finally:
            return JsonResponse(res)
    return render(request, 'menu/add.html', locals())

def MenuDetail(request, id):
    menu = Menu.objects.get(pk=id)
    return render(request, 'menu/detail.html', locals())

def MenuUpdate(request, id):
    if request.method == 'POST':
        try:
            post_data = {key: value for key, value in request.POST.items() if value and key != 'csrfmiddlewaretoken'}
            Menu.objects.filter(pk=id).update(**post_data)
            res = {'code': 1, 'msg': '模块已更新！'}
        except Exception as e:
            res = {'code': 0, 'msg': str(e)}
        finally:
            return JsonResponse(res)
    menu = Menu.objects.get(pk=id)
    return render(request, 'menu/update.html', locals())

def MenuDelete(request, id):
    try:
        Menu.objects.filter(pk=id).delete()
        res = {'code': 1, 'msg': '模块已删除！'}
    except Exception as e:
        res = {'code': 0, 'msg': str(e)}
    finally:
        return JsonResponse(res)

def UserList(request):
    roles = Role.objects.all()
    return render(request, 'user/list.html', locals())

def UserListAPI(request):
    # 查询处理
    search_filter = request.GET.get('search_filter', '')
    role = request.GET.get('role', '')
    q = Q(username__icontains=search_filter) | Q(email__icontains=search_filter)
    if role:
        user_set = User.objects.select_related().filter(role__name__icontains=role).filter(q).distinct()
    else:
        user_set = User.objects.select_related().filter(q).distinct()

    # 构造返回数据结构
    user_list = []
    for user in user_set:
        roles = []
        for role in user.role_set.all():
            roles.append(role.name)
        user_instance = {'id': user.id, 'username': user.username, 'email': user.email, 'roles': roles, \
        'is_active': '已激活' if user.is_active else '未激活', 'phone': user.profile.phone, \
        'wechat': user.profile.wechat, 'comment': user.profile.comment, \
        'last_login': (user.last_login + datetime.timedelta(hours=8)).strftime( '%Y-%m-%d %H:%M:%S' ) \
        if user.last_login else user.last_login}
        user_list.append(user_instance)
    
    # 分页处理
    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 10)
    count, data = my_paginator(user_list, page, limit)

    res = {'code': 0, 'msg': '', 'count': count, 'data': data}
    return JsonResponse(res)

def UserAdd(request):
    roles = Role.objects.all()
    groups = Group.objects.all()
    if request.method == 'POST':
        try:
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            email = request.POST.get('email', '')
            is_active = request.POST.get('is_active', 1)
            user = User.objects.create(username=username, email=email, is_active=is_active)
            user.set_password(password)
            user.profile.phone = request.POST.get('phone', '')
            user.profile.wechat = request.POST.get('wechat', '')
            user.profile.comment = request.POST.get('comment', '')
            user.save()
            user.role_set.set(request.POST.getlist('roles[]', []))
            user.groups.set(request.POST.getlist('groups[]', []))
            res = {'code': 1, 'msg': '用户已经创建！'}
        except Exception as e:
            res = {'code': 0, 'msg': str(e)}
        return JsonResponse(res)
    return render(request, 'user/add.html', locals()) 

def UserDetail(request, id):
    user = User.objects.get(pk=id)
    roles = ', '.join([role.name for role in user.role_set.all()])
    groups = ', '.join([group.name for group in user.groups.all()])
    return render(request, 'user/detail.html', locals())

def UserSet(request):
    return render(request, 'user/set.html', locals())

def UserProfile(request, id):
    user = User.objects.get(pk=id)
    roles = ', '.join([role.name for role in user.role_set.all()])
    # groups = ', '.join([group.name for group in user.groups.all()])
    return render(request, 'user/profile.html', locals())

def UserUpdate(request, id):
    user = User.objects.get(pk=id)
    if request.method == 'POST':
        try:
            # pprint.pprint(request.POST)
            user.username = request.POST.get('username', '')
            user.email = request.POST.get('email', '')
            user.is_active = request.POST.get('is_active', 0)
            user.profile.phone = request.POST.get('phone', '')
            user.profile.wechat = request.POST.get('wechat', '')
            user.profile.comment = request.POST.get('comment', '')
            user.save()
            user.role_set.set(request.POST.getlist('roles[]', []))
            user.groups.set(request.POST.getlist('groups[]', []))
            res = {'code': 1, 'msg': '用户已经更新！'}
        except Exception as e:
            res = {'code': 0, 'msg': str(e)}
        return JsonResponse(res)
    roles = Role.objects.all()
    groups = Group.objects.all()
    return render(request, 'user/update.html', locals())

def ResetPass(request, id):
    user = User.objects.get(pk=id)
    try:
        password = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        user.set_password(password)
        user.save()
        res = {'code': 1, 'msg': '重置成功！当前密码：%s'%(password)}
    except Exception as e:
        res = {'code': 0, 'msg': str(e)}
    return JsonResponse(res)

def ChangePass(request, id):
    if request.method == 'POST':
        try:
            user = User.objects.get(pk=id)
            old_password = request.POST.get('old_password', '')
            user = authenticate(username=request.user.username, password=old_password)
            if user:
                new_password = request.POST.get('new_password', '')
                new_password1 = request.POST.get('new_password1', '')
                if new_password == new_password1:
                    user.set_password(new_password)
                    user.save()
                    res = {'code': 1, 'msg': '修改密码成功'}
                else:
                    res = {'code': 0, 'msg': '两次输入密码不一致'}
            else:
                res = {'code': 0, 'msg': '旧密码错误'}
        except Exception as e:
            res = {'code': 0, 'msg': str(e)}
        return JsonResponse(res)
    return render(request, 'user/change_pass.html')

def UserDelete(request, id):
    try:
        user = User.objects.get(pk=id)
        if user.is_superuser:
            res = {'code': 0, 'msg': '超级管理员,禁止删除'}
        else:
            User.objects.filter(pk=id).delete()
            res = {'code': 1, 'msg': '删除成功 ！'}
    except Exception as e:
        res = {'code': 0, 'msg': str(e)}
    return JsonResponse(res)

def RoleList(request):
    roles = Role.objects.all()
    return render(request, 'role/list.html', locals())

def RoleAdd(request):
    if request.method == "POST":
        try:
            name = request.POST.get('name', '')
            code = request.POST.get('code', '')
            role = Role.objects.create(name=name, code=code)
            res = {'code': 1, 'msg': '角色已经创建！'}
        except Exception as e:
            res = {'code': 0, 'msg': str(e)}
        return JsonResponse(res)
    return render(request, 'role/add.html', locals())

def RoleUpdate(request, id):
    role = Role.objects.get(pk=id)
    if request.method == "POST":
        try:
            role.name = request.POST.get('name', '')
            role.save()
            role.users.set(request.POST.getlist('users[]', []))
            res = {'code': 1, 'msg': '角色已经更新！'}
        except Exception as e:
            res = {'code': 0, 'msg': str(e)}
        return JsonResponse(res)
    users = User.objects.all()
    return render(request, 'role/update.html', locals())

def RoleDelete(request, id):
    try:
        Role.objects.filter(pk=id).delete()
        res = {'code': 1, 'msg': '删除成功 ！'}
    except Exception as e:
        res = {'code': 0, 'msg': str(e)}
    return JsonResponse(res)

def PermList(request):
    # 查询处理
    search_filter = request.GET.get('search_filter', '')
    role_selected = request.GET.get('role', '')
    q = Q(module__icontains=search_filter) | Q(name__icontains=search_filter)

    perms = Perm.objects.select_related().filter(q).distinct().order_by('id')
    roles = Role.objects.order_by('id')

    # 构造返回数据结构
    if role_selected:
        all_role = Role.objects.filter(pk=role_selected)
        role_selected = all_role[0]
    else:
        all_role = roles

    perm_list = []
    for perm in perms:
        row = {'perm_id': perm.id, 'perm_module': perm.module, 'perm_name': perm.name}
        role_list = []
        for role in all_role:
            if role in perm.role_set.all():
                role_list.append(role.id)
            else:
                role_list.append(0)
        row['roles'] = role_list
        perm_list.append(row)
    
    return render(request, 'perm/list.html', locals())

def PermUpdate(request):
    if request.method == 'POST':
        try:
            # querydict转换成字典
            post_data = request.POST.dict()

            del post_data['csrfmiddlewaretoken']

            # 一个权限对应多个角色
            from collections import defaultdict
            d = defaultdict(list)
            for item in post_data.keys():
                perm_id, role_id = item.split('-')
                d[perm_id].append(int(role_id))
            # print(d)
            
            # 给权限添加角色
            for perm, roles in d.items():
                perm_obj = Perm.objects.get(pk=perm)
                perm_obj.role_set.set(roles)

            res = {'code': 1, 'msg': '保存成功 ！'}
        except Exception as e:
            res = {'code': 0, 'msg': str(e)}
        return JsonResponse(res)

    # 查询处理
    perms = Perm.objects.order_by('id')
    all_role = Role.objects.order_by('id')

    # 构造返回数据结构
    perm_list = []
    for perm in perms:
        row = {'perm_id': perm.id, 'perm_module': perm.module, 'perm_name': perm.name}
        role_list = []
        for role in all_role:
            if role in perm.role_set.all():
                role_list.append({'status': True, 'id': role.id})
            else:
                role_list.append({'status': False, 'id': role.id})
        row['roles'] = role_list
        perm_list.append(row)
    
    return render(request, 'perm/update.html', locals())

def ServiceList(request):
    services = Service.objects.all()
    return render(request, 'service/list.html', locals())

def ServiceUpdate(request, id):
    if request.method == 'POST':
        try:
            post_data = { key: value for key, value in request.POST.items() if key != 'csrfmiddlewaretoken' }
            Service.objects.filter(pk=id).update(**post_data)
            res = {'code': 1, 'msg': '服务配置已经更新！'}
        except Exception as e:
            res = {'code': 0, 'msg': str(e)}
        return JsonResponse(res)
    service = Service.objects.get(pk=id)
    return render(request, 'service/update.html', locals())