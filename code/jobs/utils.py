# -*- coding: utf-8 -*-
# @Author: yangwei
# @Date:   2018-03-22 11:06:05
# @Last Modified by:   yangwei
# @Last Modified time: 2018-03-26 18:25:13

from dataPlus.settings import SALT_IP, SALT_PORT, SALT_USER, SALT_PASSWD
from dataPlus.settings import mongo as MONGO_CLIENT 
from .saltapi import SaltAPI
import time
import os

def Cmd(user, client, target, arg_list):
    result, error = {}, ''
    try:
        salt = SaltAPI(SALT_IP, SALT_USER, SALT_PASSWD, SALT_PORT)
        result = salt.run(fun='cmd.run', target=target, arg_list=arg_list)
        job = {'user':user, 'time':time.strftime("%Y-%m-%d %X", time.localtime()), 'client':client, \
        'target':target, 'fun':'cmd.run', 'arg':arg_list, \
        'status':'', 'progress':'Finish', 'result': str(result), 'cjid':str(int(round(time.time() * 1000)))}
        MONGO_CLIENT.dataPlus.joblist.insert_one(job)
    except Exception as e:
        error = str(e)
    return result, error

def upload_file(file, destination="/tmp"):
    error = ''
    try:
        f = open(os.path.join(destination, file.name), 'wb+') 
        for chunk in file.chunks():
            f.write(chunk)  
        f.close()
        if "tar" in file.name:
            os.system('tar xvf %s -C %s'%(os.path.join(destination, file.name), destination))
            os.remove(os.path.join(destination, file.name))
    except Exception as e:
        error = str(e)
    return error

def run_script(user, client, target, arg_list, async=False):
    result = {}
    error = ''
    try:
        arg_list = 'salt://scripts/' + arg_list
        salt = SaltAPI(SALT_IP, SALT_USER, SALT_PASSWD, SALT_PORT)
        if async:
            result = salt.run_async(fun='cmd.script', target=target, arg_list=arg_list)
            job = {'user':user, 'time':time.strftime("%Y-%m-%d %X", time.localtime()), 'client':client, \
            'target':target, 'fun':'cmd.script', 'arg':arg_list, 'progress':'', 'jid':result['jid']}
        else:
            result = salt.run(fun='cmd.script', target=target, arg_list=arg_list)
            job = {'user':user, 'time':time.strftime("%Y-%m-%d %X", time.localtime()), 'client':client, \
            'target':target, 'fun':'cmd.script', 'arg':arg_list, \
            'status':'', 'progress':'Finish', 'result': str(result), 'cjid':str(int(round(time.time() * 1000)))}
        MONGO_CLIENT.dataPlus.joblist.insert_one(job)
    except Exception as e:
        error = str(e)
    return result, error

def push_file(user, client, target, arg_list):
    result = {}
    error = ''
    try:
        arg_list[0] = 'salt://files/' + arg_list[0]
        salt = SaltAPI(SALT_IP, SALT_USER, SALT_PASSWD, SALT_PORT)
        result = salt.run(fun='cp.get_file', target=target, arg_list=arg_list)
        job = {'user':user, 'time':time.strftime("%Y-%m-%d %X", time.localtime()), 'client':client, \
        'target':target, 'fun':'push file to minion', 'arg':' '.join(arg_list), \
        'status':'', 'progress':'Finish', 'result': str(result), 'cjid':str(int(round(time.time() * 1000)))}
        MONGO_CLIENT.dataPlus.joblist.insert_one(job)
    except Exception as e:
        error = str(e)
    return result, error

def state_deploy(user, client, target, arg_list, async=False):
    result = {}
    error = ''
    try:
        arg_list = 'states/' + arg_list
        salt = SaltAPI(SALT_IP, SALT_USER, SALT_PASSWD, SALT_PORT)
        if async:
            result = salt.run_async(fun='state.sls', target=target, arg_list=arg_list)
            job = {'user':user, 'time':time.strftime("%Y-%m-%d %X", time.localtime()), 'client':client, \
            'target':target, 'fun':'state.sls', 'arg':arg_list, 'progress':'', 'jid':result['jid']}
        else:
            ret = salt.run(fun='state.sls', target=target, arg_list=arg_list)
            result = {}
            for key,value in ret.items():
                tmp = {'process':{}, 'summary':{}}
                succeeded = 0
                failed = 0
                total_duration = 0
                for k,v in value.items():
                    tmp1 = k.split('_|-')
                    fun = '.'.join([tmp1[0], tmp1[3]])
                    v['fun'] = fun
                    v['id'] = tmp1[1]
                    tmp['process'].update({str(v['__run_num__']):v})
                    if v['result'] == True:
                        succeeded += 1
                    else:
                        failed += 1
                    total_duration += v['duration']
                tmp['summary'].update({'succeeded':succeeded, 'failed':failed, 'total_duration':total_duration})
                result[key] = tmp
            job = {'user':user, 'time':time.strftime("%Y-%m-%d %X", time.localtime()), 'client':client, \
            'target':target, 'fun':'state.sls', 'arg':arg_list, \
            'status':'', 'progress':'Finish', 'result': str(result), 'cjid':str(int(round(time.time() * 1000)))}
        MONGO_CLIENT.dataPlus.joblist.insert_one(job)
    except Exception as e:
        error = str(e)
    return result, error