# -*- coding: utf-8 -*-
# @Author: yangwei
# @Date:   2018-03-05 15:32:05
# @Last Modified by:   yangwei
# @Last Modified time: 2018-03-26 13:13:20
# @run method: python manage.py runscript init

from django.contrib.auth.models import User, Group
from admins.models import Role, Perm, Service, Menu

menu_list = [
    {
        'name': '主机管理',
        'code': 'host',
        'url': '/cmdb/host/index',
        'is_nav': True
    },
    {
        'name': '作业平台',
        'code': 'jobs',
        'url': '/jobs/index',
        'is_nav': True
    },
    {
        'name': '平台管理',
        'code': 'admins',
        'url': '/admins',
        'is_nav': False
    }
]

for menu in menu_list:
    try:
        Menu.objects.update_or_create(code=menu['code'], defaults={'name': menu['name'], 'url': menu['url'], 'is_nav': menu['is_nav']})
    except Exception as e:
        print('**************   Error: create menu  **************')
        print(str(e))
        print('****************************************************')
        break

perms_list = [
    {
        '用户管理':
            [
                {'name': '新建用户', 'code': 'c_user'},
                {'name': '查询用户', 'code': 'r_user'},
                {'name': '更新用户', 'code': 'u_user'},
                {'name': '删除用户', 'code': 'd_user'}
            ]
    },
    {
        '权限列表':
            [
                {'name': '查询权限', 'code': 'r_perm'},
                {'name': '更新权限', 'code': 'u_perm'}
            ],
        '角色管理':
            [
                {'name': '新建角色', 'code': 'c_role'},
                {'name': '查询角色', 'code': 'r_role'},
                {'name': '更新角色', 'code': 'u_role'},
                {'name': '删除角色', 'code': 'd_role'}
            ]
    },
    {
        '服务管理':
            [
                {'name': '查询服务', 'code': 'r_service'},
                {'name': '更新服务', 'code': 'u_service'}
            ]
    },
    {
        '资源模型':
            [
                {'name': '新建模型', 'code': 'c_model'},
                {'name': '查询模型', 'code': 'r_model'},
                {'name': '更新模型', 'code': 'u_model'},
                {'name': '删除模型', 'code': 'd_model'},
                {'name': '新建属性', 'code': 'c_field'},
                {'name': '查询属性', 'code': 'r_field'},
                {'name': '更新属性', 'code': 'u_field'},
                {'name': '删除属性', 'code': 'd_field'}
            ],
        '主机管理':
            [
                {'name': '添加主机', 'code': 'c_host'},
                {'name': '查询主机', 'code': 'r_host'},
                {'name': '更新主机', 'code': 'u_host'},
                {'name': '删除主机', 'code': 'd_host'},
                {'name': '导入主机', 'code': 'import_host'},
                {'name': '导出主机', 'code': 'export_host'}
            ]
    },
    {
        '作业平台':
            [
                {'name': '命令执行', 'code': 'run_cmd'},
                {'name': '文件传输', 'code': 'push_file'},
                {'name': '上传文件', 'code': 'upload_file'},
                {'name': '删除文件', 'code': 'delete_file'},
                {'name': '执行脚本', 'code': 'run_script'},
                {'name': '执行模块', 'code': 'run_state'},
                {'name': '添加定时任务', 'code': 'c_cron'},
                {'name': '删除定时任务', 'code': 'd_cron'}
            ]
    }
]

for item in perms_list:
    try:
        for module, perms in item.items():
            for perm in perms:
                permission, status = Perm.objects.update_or_create(module=module, name=perm['name'], code=perm['code'])
    except Exception as e:
        print('**************Error: create permission**************')
        print(str(e), 'create permission')
        print('****************************************************')
        break

role_list = [('管理员', 'admin'), ('运维', 'ops'), ('测试', 'test'), ('开发', 'dev'), ('普通用户', 'common')]
for r in role_list:
    try:
        role, role_created = Role.objects.get_or_create(name=r[0], code=r[1])
        if role:
            if role.code == 'admin':
                perms = Perm.objects.all()
                role.perms.set(perms)
    except Exception as e:
        print('**************   Error: create roles  **************')
        print(str(e))
        print('****************************************************')
        break


admin_user_list = [{'username': 'admin', 'password': 'admin@123'}]
try:
    for user in admin_user_list:
        user_instance, created = User.objects.get_or_create(username=user['username'], defaults={'is_superuser': True})
        if created:
            user_instance.set_password(user['password'])
            user_instance.save()
        if user_instance:
            role, role_created = Role.objects.get_or_create(name='管理员')
            if role:
                role.users.add(user_instance)
except Exception as e:
  print('**************   Error: create admin user  **************')
  print(str(e))
  print('****************************************************')

service_list = [
    {
    'name': 'webssh',
    'host': '0.0.0.0',
    'port': 9527,
    'comment': 'web终端服务'
    },
    {
    'name': 'ftp',
    'host': '0.0.0.0',
    'port': 80,
    'comment': '文件服务器'
    }
]
for service in service_list:
    try:
        Service.objects.get_or_create(name=service['name'], defaults={'host': service['host'], 'port': service['port'], 'comment': service['comment']})
    except Exception as e:
        print('**************   Error: create service  **************')
        print(str(e))
        print('****************************************************')
        break

from cmdb.models import Category, Prop
c_list = [
    {
        'name': '主机',
        'code': 'host',
        'props': [
            {
                'code': 'hostname',
                'name': '主机名',
                'is_must': True,
            },
            {
                'code': 'ip',
                'name': 'IP地址',
                'is_must': True,
            },
            {
                'code': 'os',
                'name': '操作系统',
                'is_must': True,
            },
            {
                'code': 'cpu',
                'name': '处理器',
                'is_must': True,
            },
            {
                'code': 'mem',
                'name': '内存',
                'is_must': True,
            },
            {
                'code': 'eth',
                'name': '网卡',
                'is_must': True,
            },
            {
                'code': 'is_virtual',
                'name': '虚拟/物理',
                'is_must': True,
            },
            {
                'code': 'minion_status',
                'name': 'salt客户端状态',
                'is_must': True,
            }
        ] 
    }
]
for c in c_list:
    try:
        category, created = Category.objects.get_or_create(name=c['name'], code=c['code'])
        # if created:
        for p in c['props']:
            prop, marked = Prop.objects.get_or_create(**p)
            category.props.add(prop)
    except Exception as e:
        print('**************   Error: create category  **************')
        print(str(e))
        print('****************************************************')
    

# from devops.settings import scheduler
# from ops.jobs import check_minion_status,update_grains
# try:
#     job1 = scheduler.cron('*/10 * * * *',func=check_minion_status,args=['','',['all'],'checking minions status'],repeat=None,queue_name='default')
#     print job1
#     job2 = scheduler.cron('0 0 */3 * *',func=update_grains,args=['','',['all'],'updating grains'],repeat=None,queue_name='default')
#     print job2
# except Exception as e:
#     print e
