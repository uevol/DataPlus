from django.shortcuts import render
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
import json
from utils.paginator import my_paginator
from django.db.models import Q
from admins.models import Service
from dataPlus.settings import mongo
import datetime as dt
import xlsxwriter
import io
import xlrd
# Create your views here.

def HostIndex(request):
    return render(request, 'host/index.html')

@csrf_exempt
def CreateOrUpdateHostAPI(request):
    ''' create or update host according to posted data from salt '''
    try:
        data = json.loads(request.body)
        category_id = Category.objects.get(code='host').id
        data['category_id'] = category_id
        base = {'category_id': category_id, 'hostname': data['hostname'], 'ip': data['ip'], \
        'is_virtual': data['is_virtual'], 'mem': data['mem'], 'minion_status': data['minion_status'], \
        'os': data['os'], 'salt_key': data['salt_key'], 'cpu': data['cpu']}
        obj, created = Host.objects.update_or_create(minion_id=data['minion_id'], defaults=base)
        res = {'time':dt.datetime.now().strftime("%Y:%m:%d %H:%M:%S"), 'ip': data['ip'], 'salt_key': data['salt_key']}
        if created:
            res.update({ 'code': 1, 'msg': 'host created'})
        else:
            res.update({'code': 1, 'msg': 'host updated'})
        mongo.dataPlus.host.update({'minion_id':data['minion_id']}, {'$set': data, \
            "$currentDate": {"lastModified": True}}, upsert=True)
    except Exception as e:
        res.update({'code': 0, 'error': str(e)})
    return JsonResponse(res)

def HostList(request):
    category = Category.objects.get(code='host')
    custom_field = [{'name':prop.name, 'code':prop.code, 'optional':prop.get_optional_value()} \
        for prop in category.props.filter(is_must=False)]
    return render(request, 'host/list.html', locals())

def HostListAPI(request):
    # 查询处理
    search_filter = request.GET.get('search_filter', '')
    q = Q(ip__icontains=search_filter) | Q(hostname__icontains=search_filter) | Q(admins__username__icontains=search_filter)
    hosts = Host.objects.select_related().filter(q).distinct()

    # 构造返回数据结构
    host_list = []
    for host in hosts:
        host_instance = {'hostname': host.hostname, 'ip': host.ip, 'os': host.os, 'cpu': host.cpu, \
        'mem': host.mem, 'is_virtual': host.is_virtual, 'minion_status': host.minion_status, \
        'minion_id': host.minion_id, 'salt_key': host.salt_key}
        host_list.append(host_instance)
    
    # 分页处理
    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 10)
    count, data = my_paginator(host_list, page, limit)

    res = {'code': 0, 'msg': '', 'count': count, 'data': data}
    return JsonResponse(res)

def HostAdd(request):
    ftp = Service.objects.get(name='ftp')
    linux_script = "install-minion.sh"
    win_script = "windows/Salt-Minion-2016.11.7-x86-Setup.exe"
    if ftp.path:
        url = "http://%s:%s/%s/"%(ftp.host, ftp.port, ftp.path)
    else:
        url = "http://%s:%s/"%(ftp.host, ftp.port)
    return render(request, 'host/add.html', locals())

def HostModel(request):
    host = Category.objects.get(code='host')
    return render(request, 'host/model.html', locals())

def HostDetail(request, id):
    host = mongo.dataPlus.host.find_one({'minion_id': id})
    category = Category.objects.get(code='host')
    # lastModified = host['lastModified'].strftime('%Y:%m:%d %H:%M:%S')
    custom_field = [{'name':prop.name, 'code':prop.code, 'value':host.get(prop.code, '')} \
        for prop in category.props.filter(is_must=False)]
    return render(request, 'host/detail.html', locals())

def HostUpdate(request, id):
    if request.method == "POST":
        try:
            dct = request.POST.dict()
            dct.pop('csrfmiddlewaretoken')
            host = mongo.dataPlus.host.update_one({'minion_id': id}, {'$set': dct, \
                "$currentDate": {"lastModified": True}})
            res = {'code': 1, 'msg': '主机信息更新成功'}
        except Exception as e:
            res = {'code': 0, 'msg': str(e.message)}
        finally:
            return JsonResponse(res)
    host = mongo.dataPlus.host.find_one({'minion_id': id})
    category = Category.objects.get(code='host')
    # lastModified = host['lastModified'].strftime('%Y:%m:%d %H:%M:%S')
    custom_field = [{'name':prop.name, 'code':prop.code, 'optional':prop.get_optional_value(), 'value':host.get(prop.code, '')} \
        for prop in category.props.filter(is_must=False)]
    return render(request, 'host/update.html', locals())

def HostDelete(request, id):
    try:
        Host.objects.filter(minion_id=id).delete()
        mongo.dataPlus.host.delete_one({'minion_id': id})
        res = {'code': 1, 'msg': '主机已删除！'}
    except Exception as e:
        res = {'code': 0, 'msg': str(e)}
    finally:
        return JsonResponse(res)

def HostSearch(request):
    data = { key: value for key, value in request.GET.items() if value and (key not in ['csrfmiddlewaretoken', 'page', 'limit']) }
    if data:
        query_filter = {}
        for key, value in data.items():
            query_filter[key] = {'$regex': value, '$options': 'i'}
        hosts = mongo.dataPlus.host.find(query_filter)
    else:
        hosts = mongo.dataPlus.host.find({})

    # 构造返回数据结构
    host_list = []
    for host in hosts:
        host_instance = {'hostname': host['hostname'], 'ip': host['ip'], 'os': host['os'], 'cpu': host['cpu'], \
        'mem': host['mem'], 'is_virtual': host['is_virtual'], 'minion_status': host['minion_status'], \
        'minion_id': host['minion_id'], 'salt_key': host['salt_key']}
        host_list.append(host_instance)
    
    # 分页处理
    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 10)
    count, data = my_paginator(host_list, page, limit)

    res = {'code': 0, 'msg': '', 'count': count, 'data': data}
    return JsonResponse(res)

def HostUpdateBatch(request):
    try:
        code = request.POST.get('code', '')
        value = request.POST.get('value', '')
        ids = request.POST.get('hosts', '')
        host = mongo.dataPlus.host.update_many({'minion_id': {'$in': ids.split(',')}}, {'$set': {code: value}, \
            "$currentDate": {"lastModified": True}})
        res = {'code': 1, 'msg': '批量更新成功'}
    except Exception as e:
        res = {'code': 0, 'msg': str(e)}
    finally:
        return JsonResponse(res)

def HostExport(request):
    ids = request.POST.get('ids', '')
    hosts = mongo.dataPlus.host.find({'minion_id': {'$in': ids.split(',')}})
    category = Category.objects.get(code='host')
    fields = ['minion_id'] + [prop.code for prop in category.props.all()]
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()
    worksheet.write_row('A1', fields)
    row = 2
    for host in hosts:
        data = [host[field] for field in fields]
        worksheet.write_row('A'+str(row), data)
        row +=1
    workbook.close()
    output.seek(0)
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")  
    response['Content-Disposition'] = 'attachment; filename=%s.xlsx' % dt.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") 
    return response

def HostImport(request):
    if request.method == "POST":
        try:
            myFile = request.FILES.get("file", None)
            wb = xlrd.open_workbook(file_contents=myFile.read())
            table = wb.sheets()[0]
            rows = table.nrows
            category = Category.objects.get(code='host')
            fields = ['minion_id'] + [prop.code for prop in category.props.all()]
            for i in range(1, rows):
                try:
                    data = { code: value for code, value in zip(fields, table.row_values(i))}
                    mongo.dataPlus.host.update({'minion_id':data['minion_id']}, {'$set': data, \
                "$currentDate": {"lastModified": True}}, upsert=True)
                except Exception as e:
                    res = {'code': 0, 'msg': '导入停止，原因：'%(data['ip']+str(e))}
                    break
                    return JsonResponse(res)
            res = {'code': 1, 'msg': '导入完成'}
        except Exception as e:
            res = {'code': 0, 'msg': str(e)}
        finally:
            return JsonResponse(res)
    return render(request, 'host/host_import.html', locals())

def HostAddProp(request):
    if request.method == "POST":
        try:
            host = Category.objects.get(code='host')
            dct = request.POST.dict()
            dct.pop('csrfmiddlewaretoken')
            prop = Prop.objects.create(**dct)
            host.props.add(prop)
            res = {'code': 1, 'msg': '字段已添加！'}
        except Exception as e:
            res = {'code': 0, 'msg': str(e)}
        finally:
            return JsonResponse(res)
    return render(request, 'host/add_prop.html', locals())

def HostDelProp(request, id):
    try:
        prop = Prop.objects.get(pk=id)
        host = Category.objects.get(code='host')
        host.props.remove(prop)
        prop.delete()
        res = {'code': 1, 'msg': '字段已删除！'}
    except Exception as e:
        res = {'code': 0, 'msg': str(e)}
    finally:
        return JsonResponse(res)

def HostUpdateProp(request, id):
    if request.method == "POST":
        try:
            dct = request.POST.dict()
            dct.pop('csrfmiddlewaretoken')
            Prop.objects.filter(pk=id).update(**dct)
            res = {'code': 1, 'msg': '字段已更新！'}
        except Exception as e:
            res = {'code': 0, 'msg': str(e)}
        finally:
            return JsonResponse(res)
    prop = Prop.objects.get(pk=id)
    return render(request, 'host/update_prop.html', locals())
