# @Time    : 2019/2/15 14:02
# @Author  : xufqing

import os, yaml, logging, nmap
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest_xops.settings')
error_logger = logging.getLogger('error')

class ConfigFileMixin:
    config_file = None

    def get_config_file(self):
        """
        获取配置文件
        """
        if self.config_file is None:
            msg = ' %(cls)s 未定义配置文件路径，需定义config_file的值' % {'cls': self.__class__.__name__}
            error_logger.error(msg)
            raise ValueError(msg)
        return self.config_file

    def get_conf_content(self, *key):
        """
        获取配置文件对应的key
        """
        _config = self.get_config_file()
        with open(_config) as f:
            content = yaml.load(f)
        if key is not None:
            try:
                num = 0
                while num < len(key):
                    content = content[key[num]]
                    num += 1
            except Exception as e:
                msg = '%(config)s 没有%(exc)s 这个值' % {
                    'exc': e,
                    'config': _config
                }
                error_logger.error(msg)
                raise ValueError(msg)
        return content


class ScanSettingsLoad(ConfigFileMixin):
    '''
    加载扫描设置
    '''
    config_file = os.path.join(settings.YML_CONF_DIR, 'scan_settings.yml')

    def get_net_address(self):
        hosts_list = self.get_conf_content('hosts', 'net_address')
        hosts = ' '.join(str(i) for i in hosts_list)
        return hosts

    def get_ssh_port(self):
        return self.get_conf_content('hosts', 'ssh_port')

    def os_scan(self):
        hosts = self.get_net_address()
        port = self.get_ssh_port()
        nm = nmap.PortScanner()
        nm.scan(hosts=hosts, ports=port, arguments='-T4 -sS -Pn')
        online_hosts = []
        for host in nm.all_hosts():
            open = nm._scan_result['scan'][host]['tcp'][int(port)]['state']
            if open == 'open':
                try:
                    name = nm._scan_result['scan'][host]['tcp'][int(port)]['name']
                except Exception:
                    name = 'unknown'
                host_dict = {'host': host, 'os': name, 'open':open}
                online_hosts.append(host_dict)
        return online_hosts

def excludes_format(path, excludes_string=None):
    '''
    排除文件，支持正则匹配，支持多选字符串
    '''
    if not excludes_string:
        return path

    prefix = '--exclude='
    excludes = [prefix + i for i in excludes_string.split('\n') if i.strip()]

    return ' {excludes} {path} '.format(excludes=' '.join(excludes), path='--exclude=.git --exclude=.gitignore .')


def includes_format(path, includes_string=None):
    '''
    指定发布文件，支持正则匹配，如：*.war。支持多行字符串。
    '''
    if not includes_string:
        return path
    includes = []

    for i in includes_string.split('\n'):
        i = i.strip()
        if i:
            patha = os.path.split(i)
            includes.append(patha)
    if not includes:
        return path

    return includes
