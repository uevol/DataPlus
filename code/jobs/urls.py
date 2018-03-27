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

app_name='jobs'
urlpatterns = [
    path('index', views.JobIndex, name='JobIndex'),
    path('cmd', views.JobCmd, name='JobCmd'),
    path('scripts/list', views.ScriptIndex, name='ScriptIndex'),
    path('scripts/list/api', views.ScriptListAPI, name='ScriptListAPI'),
    path('file/upload', views.UploadFile, name='UploadFile'),
	re_path(r'file/delete/(?P<id>\d+)/$', views.DeleteFile, name='DeleteFile'),
	re_path(r'file/view/(?P<id>\d+)/$', views.ViewFile, name='ViewFile'),
	re_path(r'script/run/(?P<id>\d+)/$', views.ScriptRun, name='ScriptRun'),
	path('files/list', views.FileIndex, name='FileIndex'),
	path('files/list/api', views.FileListAPI, name='FileListAPI'),
	re_path(r'file/push/(?P<id>\d+)/$', views.FilePush, name='FilePush'),
	path('states/list', views.StateIndex, name='StateIndex'),
	path('states/list/api', views.StateListAPI, name='StateListAPI'),
	re_path(r'state/deploy/(?P<id>\d+)/$', views.StateDeploy, name='StateDeploy'),
	path('cron/list', views.CronIndex, name='CronIndex'),
	path('cron/list/api', views.CronListAPI, name='CronListAPI'),
	path('cron/add', views.CronAdd, name='CronAdd'),
	re_path(r'cron/delete/(?P<id>.+)/$', views.CronDelete, name='CronDelete'),
	path('result/list', views.JobList, name='JobList'),
	path('result/list/api', views.JobListAPI, name='JobListAPI'),
	re_path(r'result/detail/(?P<jid>.+)/$', views.JobResult, name='JobResult'),
]
