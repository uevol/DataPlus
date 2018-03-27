from django.shortcuts import render
from .utils import Cmd, upload_file, run_script, push_file, state_deploy
from django.http import JsonResponse
from utils.paginator import my_paginator
from django.db.models import Q
from .models import *
from dataPlus.settings import MEDIA_ROOT
import os
import time
import datetime
from dataPlus.settings import scheduler
from dataPlus.settings import mongo
# Create your views here.

def JobIndex(request):
    return render(request, 'jobs/index.html')

def JobCmd(request):
    if request.method == "POST":
        try:
            user = request.user.username
            if 'HTTP_X_FORWARDED_FOR' in request.META:
                client =  request.META['HTTP_X_FORWARDED_FOR']  
            else:
                client = request.META['REMOTE_ADDR']
            hosts = request.POST.get('hosts', [])
            host_nums = len(hosts.split(','))
            command = request.POST.get('command', '')
            ret, error = Cmd(user, client, hosts, command)
        except Exception as e:
            error = str(e)
    return render(request, 'cmd/index.html', locals())

def UploadFile(request):
    ''' Upload file to remote salt-master server '''
    if request.method == "POST":
        try:
            file = request.FILES.get("file", None)
            file_type = request.POST.get('file_type', '')
            user = request.user.username
            if 'HTTP_X_FORWARDED_FOR' in request.META:
                client =  request.META['HTTP_X_FORWARDED_FOR']
            else:
                client = request.META['REMOTE_ADDR']
            if file_type == 'other':
                myfile, updated = File.objects.update_or_create(code=file.name, name=file.name, defaults={'created_by':user})
                res = upload_file(file, os.path.join(MEDIA_ROOT, 'files'))
            elif file_type == 'script':
                myfile, updated = File.objects.update_or_create(code=file.name, name=file.name, \
                    file_type='script', defaults={'created_by':user})
                res = upload_file(file, os.path.join(MEDIA_ROOT, 'scripts'))
            else:
                myfile, updated = File.objects.update_or_create(code=file.name, name=file.name, \
                    file_type='state', defaults={'created_by':user})
                res = upload_file(file, os.path.join(MEDIA_ROOT, 'states'))
            if res:
                myfile.delete()
                res = {'code': 0, 'msg': res}
            else:
                res = {'code': 1, 'msg': '文件上传成功', 'filename': file.name }
        except Exception as e:
            res = {'code': 0, 'msg': str(e)}
    return JsonResponse(res)

def ViewFile(request, id):
    try:
        script = File.objects.get(pk=id)
        file = os.path.join(MEDIA_ROOT, 'scripts', script.code)
        f = open(file,'r')
        context = f.read()
        f.close()
    except Exception as e:
        context = str(e)
    return render(request,'scripts/context.html',locals())

def DeleteFile(request, id):
    ''' Delete file '''
    try:
        File.objects.filter(pk=id).delete()
        res = {'code': 1, 'msg': '删除成功 ！'}
    except Exception as e:
        res = {'code': 0, 'msg': str(e)}
    return JsonResponse(res)

def ScriptIndex(request):
    return render(request, 'scripts/index.html')

def ScriptListAPI(request):
    ''' script list  API'''
    keyword = request.GET.get('keyword', '')
    if keyword:
        q = Q(code__icontains=keyword) | Q(name__icontains=keyword)
        scripts = File.objects.filter(file_type='script').filter(q)
    else:
        scripts = File.objects.filter(file_type='script')
    data = [{'id': script.id, 'code': script.code, 'name': script.name, 'file_type': script.file_type, 'created_by': script.created_by, \
    'comment': script.comment, 'create_time': script.create_time.strftime("%Y:%m:%d %H:%M:%S"), 'update_time': script.update_time.strftime("%Y:%m:%d %H:%M:%S")} for script in scripts ]
    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 10)
    count, data = my_paginator(data, page, limit)

    res = {'code': 0, 'msg': '', 'count': count, 'data': data}
    return JsonResponse(res)

def ScriptRun(request, id):
    script = File.objects.get(pk=id)
    if request.method == "POST":
        try:
            hosts = request.POST.get('hosts')
            host_nums = len(hosts.split(','))
            if 'HTTP_X_FORWARDED_FOR' in request.META:
                client =  request.META['HTTP_X_FORWARDED_FOR']  
            else:
                client = request.META['REMOTE_ADDR']
            user = request.user.username
            ret, error = run_script(user, client, hosts, script.code)
        except Exception as e:
            error = str(e)
    return render(request,'scripts/run.html',locals())

def FileIndex(request):
    return render(request, 'files/index.html')

def FileListAPI(request):
    ''' script list  API'''
    keyword = request.GET.get('keyword', '')
    if keyword:
        q = Q(code__icontains=keyword) | Q(name__icontains=keyword)
        scripts = File.objects.filter(file_type='other').filter(q)
    else:
        scripts = File.objects.filter(file_type='other')
    data = [{'id': script.id, 'code': script.code, 'name': script.name, 'file_type': script.file_type, 'created_by': script.created_by, \
    'comment': script.comment, 'create_time': script.create_time.strftime("%Y:%m:%d %H:%M:%S"), 'update_time': script.update_time.strftime("%Y:%m:%d %H:%M:%S")} for script in scripts ]
    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 10)
    count, data = my_paginator(data, page, limit)

    res = {'code': 0, 'msg': '', 'count': count, 'data': data}
    return JsonResponse(res)

def FilePush(request, id):
    ''' push file to remote host(s) by saltstack '''
    if request.method == "POST":
        try:
            user = request.user.username
            if 'HTTP_X_FORWARDED_FOR' in request.META:
                client =  request.META['HTTP_X_FORWARDED_FOR']  
            else:
                client = request.META['REMOTE_ADDR']
            hosts = request.POST.get('hosts', '')
            host_nums = len(hosts.split(','))
            filename = request.POST.get('filename', '')
            remote_path = request.POST.get('remote_path', '')
            arg_list = [filename, remote_path, 'makedirs=True']
            ret, error = push_file(user, client, hosts, arg_list)
        except Exception as e:
            error = str(e)
    file = File.objects.get(pk=id)
    return render(request, 'files/push.html', locals())


def StateIndex(request):
    return render(request, 'states/index.html')

def StateListAPI(request):
    ''' script list  API'''
    keyword = request.GET.get('keyword', '')
    if keyword:
        q = Q(code__icontains=keyword) | Q(name__icontains=keyword)
        scripts = File.objects.filter(file_type='state').filter(q)
    else:
        scripts = File.objects.filter(file_type='state')
    data = [{'id': script.id, 'code': script.code, 'name': script.name, 'file_type': script.file_type, 'created_by': script.created_by, \
    'comment': script.comment, 'create_time': script.create_time.strftime("%Y:%m:%d %H:%M:%S"), 'update_time': script.update_time.strftime("%Y:%m:%d %H:%M:%S")} for script in scripts ]
    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 10)
    count, data = my_paginator(data, page, limit)

    res = {'code': 0, 'msg': '', 'count': count, 'data': data}
    return JsonResponse(res)

def StateDeploy(request, id):
    script = File.objects.get(pk=id)
    if request.method == "POST":
        try:
            hosts = request.POST.get('hosts')
            host_nums = len(hosts.split(','))
            if 'HTTP_X_FORWARDED_FOR' in request.META:
                client =  request.META['HTTP_X_FORWARDED_FOR']  
            else:
                client = request.META['REMOTE_ADDR']
            user = request.user.username
            res, error = state_deploy(user, client, hosts, script.code.split('.')[0])
        except Exception as e:
            error = str(e)
    return render(request,'states/deploy.html',locals())

def CronIndex(request):
    return render(request,'cron/index.html',locals())

def CronListAPI(request):
    job_instances = scheduler.get_jobs()
    data = [{'id':job.id, 'cron_string':job.meta['cron_string'], 'targets':','.join(job.args[2]), \
    'arg':job.args[3], 'created_at':job.created_at.strftime("%Y-%m-%d %H:%M:%S"), \
    'last_exacuted':job.ended_at.strftime("%Y-%m-%d %H:%M:%S") if job.ended_at else ''} for job in job_instances]
    
    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 10)
    count, data = my_paginator(data, page, limit)
      
    res = {'code': 0, 'msg': '', 'count': count, 'data': data}
    return JsonResponse(res)

def CronAdd(request):
    if request.method == 'POST':
        cron_string = request.POST.get('cron_string', '')
        cron_type = request.POST.get('cron_type', '')
        try:
            user = request.user.username
            if 'HTTP_X_FORWARDED_FOR' in request.META:
                client =  request.META['HTTP_X_FORWARDED_FOR']  
            else:
                client = request.META['REMOTE_ADDR']
            arg_list = request.POST.get('cmd', '') if request.POST.get('cmd', '') else 'echo hello'
            hosts = request.POST.get('hosts', '')
            target = hosts.split(',')
            print(target, hosts)
            if cron_type == 'command':
                job = scheduler.cron(cron_string, func=Cmd, args=[user, client, target, arg_list], repeat=None, queue_name='default')
            else:
                job = scheduler.cron(cron_string, func=run_script, args=[user, client, target, arg_list, True], repeat=None, queue_name='default')
            if job:
                res = {'code': 1, 'msg': '任务创建成功 ！'}
            else:
                res = {'code': 0, 'msg': '任务创建失败 ！'}
        except Exception as e:
            res = {'code': 0, 'msg': str(e)}
        return JsonResponse(res)
    return render(request,'cron/add.html',locals())

def CronDelete(request, id):
    try:
        scheduler.cancel(id)
        res = {'code': 1, 'msg': '定时任务已经删除'}
    except Exception as e:
        res = {'code': 0, 'msg': str(e)}
    return JsonResponse(res)

def JobList(request):
    ''' job list '''
    dt_till = int(time.time())
    interval = 60 * 60 * 24
    dt_from = dt_till - interval
    dt_till = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(dt_till))
    dt_from = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(dt_from))
    return render(request, 'result/index.html', locals())

def JobListAPI(request):
    ''' job list api '''
    if request.GET.get('dt_till',''):
        dt_till = request.GET.get('dt_till', '')
        dt_from = request.GET.get('dt_from', '')
    else:
        dt_till = int(time.time())
        interval = int(request.GET.get('interval','')) if request.GET.get('interval','') else 60 * 60 * 24
        dt_from = dt_till - interval
        dt_till = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(dt_till))
        dt_from = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(dt_from))
    if request.user.is_superuser:
        jobs = mongo.dataPlus.joblist.find({'time': {'$gte': dt_from, '$lte': dt_till}}).sort([('_id',-1)])
    else:
        jobs = mongo.dataPlus.joblist.find({'user':request.user.username, 'time': {'$gte': dt_from, '$lte': dt_till} }).sort([('_id',-1)])
    data = [{'user': job['user'], 'time': job['time'], 'client': job['client'], 'target': job['target'], 'fun': job['fun'], \
    'arg': job['arg'], 'progress': job['progress'], 'cjid': job['cjid'], 'status': job['status'] } for job in jobs ]
    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 10)
    count, data = my_paginator(data, page, limit)
    
    res = {'code': 0, 'msg': '', 'count': count, 'data': data}
    return JsonResponse(res)

def JobResult(request, jid):
    try:
        job = mongo.dataPlus.joblist.find_one({'cjid': jid})
        if job:
            ret = eval(job['result'])
            if job['fun'] == 'cmd.run':
                return render(request, 'result/job_cmd_result.html', locals())
            elif job['fun'] == 'cmd.script':
                return render(request, 'result/job_script_result.html', locals())
            elif job['fun'] == 'state.sls':
                return render(request, 'result/job_state_result.html', locals())
            else:
                return render(request, 'result/job_cmd_result.html', locals())
        else:
            ret = 'There is no a record in database'
    except Exception as e:
        ret = str(e)
    return render(request, 'result/result.html', locals())



















