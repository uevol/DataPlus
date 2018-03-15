#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author: uevol
# @Date:   2018-03-11 17:19:34
# @Last Modified by:   yangwei
# @Last Modified time: 2018-03-14 15:45:40
# @function: Listening Salt Master Event System and parase the job return ,then post result

import json
import datetime
import re
import multiprocessing
from multiprocessing import cpu_count

import salt.config
import salt.utils.event

# For Python 2 and 3 compatibility
try:
    import urllib2
except ImportError:
    # Since Python 3, urllib2.Request and urlopen were moved to
    # the urllib.request.
    import urllib.request as urllib2


def post_data(data, url):
    ''' post data to devops '''
    try:
        data = json.dumps(data)
        if isinstance(data, bytes):
            data = data.encode('utf-8')

        req = urllib2.Request(url, data)
        req.add_header('Content-Type', 'application/json')

        try:
            res = urllib2.urlopen(req)
            res_str = res.read().decode('utf-8')
        except Exception as e:
            res_str = str(e)
        return res_str
    except Exception as e:
        print(str(e))



def parase(event):
    try:
        pattern_job_ret = re.compile(r'salt/job/\d+/ret/.+')
        if pattern_job_ret.match(event['tag']):
            if event['data'].has_key('id') and event['data'].has_key('return'):
                data = {}
                if event['data']['fun'] == 'grains.items':
                    items = event['data']['return']
                    data['minion_id'] = str(items['server_id'])
                    data['hostname'] = items['nodename']
                    data['ip'] = [ ip for ip in items['ipv4'] if ip != '127.0.0.1'][0]
                    data['os'] = ' '.join([items['os'], items['osrelease']])
                    data['cpu'] = ' * '.join([str(items['num_cpus']), items['cpu_model']])
                    data['mem'] = items['mem_total'] / 1024 + 1
                    data['is_virtual'] = items.get('virtual', '')
                    eth = items['hwaddr_interfaces']
                    eth.pop('lo', '')
                    data['eth'] = str(eth)
                    data['salt_key'] = items['id']
                    data['minion_status'] = 'ok'
                    res = post_data(data, url='http://192.168.3.167:8000/cmdb/host/create_or_update')
                    print(res)
                elif event['data']['fun'] == 'state.sls':
                    ret = event['data']['return']
                    tmp = {'process':{},'summary':{}}
                    succeeded = 0
                    failed = 0
                    total_duration = 0
                    for k,v in ret.items():
                        tmp1 = k.split('_|-')
                        fun = '.'.join([tmp1[0],tmp1[3]])
                        v['fun'] = fun
                        v['id'] = tmp1[1]
                        tmp['process'].update({str(v['__run_num__']):v})
                        if v['result'] == True:
                            succeeded += 1
                        else:
                            failed += 1
                        total_duration += v['duration']
                    tmp['summary'].update({'succeeded':succeeded,'failed':failed,'total_duration':total_duration})
                    event['data']['return'] = str(tmp)
                    data = event['data']
                    res = post_data(data, url='http://192.168.3.167:8000/cmdb/host/create_or_update')
                    print(res)
                else:
                    pass
    except Exception as e:
        print(str(e))


if __name__ == "__main__":
    pool = multiprocessing.Pool(processes = cpu_count())
    __opts__ = salt.config.client_config('/etc/salt/master')
    event = salt.utils.event.MasterEvent(__opts__['sock_dir'])
    for eachevent in event.iter_events(full=True):
        pool.apply_async(parase, (eachevent, ))
 
    pool.close()
    pool.join()