"""dataPlus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, re_path
from django.views.generic.base import TemplateView
from . import views

app_name='admins'

urlpatterns = [
    path('', views.index, name='index'),
    path('menu/list/', views.MenuList, name='MenuList'),
    path('menu/list/api', views.MenuListAPI, name='MenuListAPI'),
    path('menu/add/', views.MenuAdd, name='MenuAdd'),
    re_path(r'^menu/detail/(?P<id>\d+)/$', views.MenuDetail, name='MenuDetail'),
    re_path(r'^menu/update/(?P<id>\d+)/$', views.MenuUpdate, name='MenuUpdate'),
    re_path(r'^menu/delete/(?P<id>\d+)/$', views.MenuDelete, name='MenuDelete'),
    path('user/list/', views.UserList, name='UserList'),
    path('user/list/api', views.UserListAPI, name='UserListAPI'),
    path('user/add/', views.UserAdd, name='UserAdd'),
    path('user/set/', views.UserSet, name='UserSet'),
    re_path(r'^user/detail/(?P<id>\d+)/$', views.UserDetail, name='UserDetail'),
    re_path(r'^user/profile/(?P<id>\d+)/$', views.UserProfile, name='UserProfile'),
    re_path(r'^user/update/(?P<id>\d+)/$', views.UserUpdate, name='UserUpdate'),
    re_path(r'^user/resetpass/(?P<id>\d+)/$', views.ResetPass, name='ResetPass'),
    re_path(r'^user/delete/(?P<id>\d+)/$', views.UserDelete, name='UserDelete'),
    re_path(r'^user/changepass/(?P<id>\d+)/$', views.ChangePass, name='ChangePass'),
    path('role/list/', views.RoleList, name='RoleList'),
    path('role/add/', views.RoleAdd, name='RoleAdd'),
    re_path(r'^role/update/(?P<id>\d+)/$', views.RoleUpdate, name='RoleUpdate'),
    re_path(r'^role/delete/(?P<id>\d+)/$', views.RoleDelete, name='RoleDelete'),
    path('perm/list/', views.PermList, name='PermList'),
    path('perm/update/', views.PermUpdate, name='PermUpdate'),
    path('service/list/', views.ServiceList, name='ServiceList'),
    re_path(r'^service/update/(?P<id>\d+)/$', views.ServiceUpdate, name='ServiceUpdate'),
]