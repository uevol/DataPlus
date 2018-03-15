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
from . import views

app_name='cmdb'
urlpatterns = [
    path('host/create_or_update', views.CreateOrUpdateHostAPI, name='CreateOrUpdateHost'),
    path('host/index', views.HostIndex, name='HostIndex'),
    path('host/list', views.HostList, name='HostList'),
    path('host/list/api', views.HostListAPI, name='HostListAPI'),
    path('host/add', views.HostAdd, name='HostAdd'),
    path('host/model', views.HostModel, name='HostModel'),
    path('host/addprop', views.HostAddProp, name='HostAddProp'),
    path('host/search', views.HostSearch, name='HostSearch'),
    path('host/hostupdatebatch', views.HostUpdateBatch, name='HostUpdateBatch'),
    re_path(r'^host/detail/(?P<id>\d+)/$', views.HostDetail, name='HostDetail'),
    re_path(r'^host/update/(?P<id>\d+)/$', views.HostUpdate, name='HostUpdate'),
    re_path(r'^host/delete/(?P<id>\d+)/$', views.HostDelete, name='HostDelete'),
    re_path(r'^host/updateprop/(?P<id>\d+)/$', views.HostUpdateProp, name='HostUpdateProp'),
    re_path(r'^host/delprop/(?P<id>\d+)/$', views.HostDelProp, name='HostDelProp'),
]