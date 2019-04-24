# @Time    : 2019/2/19 14:42
# @Author  : xufqing
import time, logging
from utils.common import ScanSettingsLoad
from utils.shell_excu import Shell
from .models import DeviceScanInfo
from rest_xops.celery import app
info_logger = logging.getLogger('info')

@app.task
def scan_execution():
    scan_settings_load = ScanSettingsLoad()
    start_time = time.time()
    auth_type = scan_settings_load.get_conf_content('hosts', 'auth_type')
    hosts = scan_settings_load.os_scan()
    login_hosts = []
    for host in hosts:
        if host['open'] == 'open':
            login_hosts.append(host)
        elif host['os'] == 'unknown':
            DeviceScanInfo.objects.update_or_create(
                hostname=host['host'],
                defaults={
                    'os_version': host['os'],
                    'os_type': 'Other'
                }
            )
    if login_hosts:
        # 从配置文件中获取登陆认证信息和认证类型
        for host in login_hosts:
            kwargs = {
                'hostname': host['host'],
                'username': scan_settings_load.get_conf_content('hosts', 'ssh_username'),
                'port': scan_settings_load.get_conf_content('hosts', 'ssh_port'),
                'commands': scan_settings_load.get_conf_content('hosts', 'commands')
            }
            if auth_type == 'password':
                kwargs['password'] = scan_settings_load.get_conf_content('hosts', 'ssh_password')
            else:
                kwargs['password'] = scan_settings_load.get_conf_content('hosts', 'ssh_private_key')
            # 将登陆执行结果数据复制给defaults
            kwargs['auth_type'] = auth_type
            kwargs['os_type'] = 'Linux'
            # 构建连接信息
            auth_info = '{user}@{host}:{port}'.format(user=kwargs['username'], host=kwargs['hostname'],port=kwargs['port'])
            auth_key = {auth_type: kwargs['password']}
            connect = Shell(auth_info, connect_timeout=5, connect_kwargs=auth_key)
            commands = kwargs['commands']
            kwargs['error_message'] = []
            for key, value in commands.items():
                result = connect.run(value)
                if hasattr(result, 'stdout'):
                    if result.failed:
                        kwargs['status'] = 'Failed'
                        kwargs['error_message'].append(str(result.stderr) + '\n')
                    else:
                        kwargs[key] = result.stdout
                        kwargs['status'] = 'Succeed'
                        kwargs['error_message'] = ''
                    continue
                else:
                    kwargs['status'] = 'Failed'
                    kwargs['error_message'] = str(result)
                    break
            connect.close()
            defaults = kwargs
            defaults.pop('commands')
            DeviceScanInfo.objects.update_or_create(
                hostname=host['host'],
                defaults=defaults
            )
    end_time = time.time()
    msg = '扫描任务已完成, 执行时间：%(time)s秒, 共%(num)s台主机.' % {
        'time': end_time - start_time,
        'num': len(hosts)
    }
    info_logger.info(msg)
