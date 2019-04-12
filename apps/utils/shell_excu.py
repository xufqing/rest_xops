# @Time    : 2019/3/7 16:19
# @Author  : xufqing
from fabric2 import Connection
from invoke import Responder, Result
from utils.websocket_tail import Tailf
import logging
from cmdb.models import DeviceInfo,ConnectionInfo

error_logger = logging.getLogger('error')
info_logger = logging.getLogger('info')


def say_yes():
    return Responder(
        pattern=r'yes/no',
        response='yes\n',
    )

def auth_init(id):
    device_info = DeviceInfo.objects.filter(id=int(id)).values()
    host = device_info[0]['hostname']
    auth_type = device_info[0]['auth_type']
    connect_info = ConnectionInfo.objects.filter(hostname=host, auth_type=auth_type).values()
    user = connect_info[0]['username']
    passwd = connect_info[0]['password']
    port = connect_info[0]['port']
    auth_info = '{user}@{host}:{port}'.format(user=user, host=host, port=port)
    auth_key = {auth_type: passwd}

    return auth_info, auth_key

class Shell(Connection):
    run_mode_remote = 'remote'
    run_mode_local = 'local'
    custom_global_env = {}

    def init_env(self, **kwargs):
        self.custom_global_env = kwargs['env']

    def run(self, command, run_mode=run_mode_remote, write=None, pty=False, exception=True, ws=False, webuser=None, **kwargs):
        try:
            if run_mode == self.run_mode_local:
                result = super(Shell, self).local(command, pty=pty, echo_stdin=True, warn=True, watchers=[say_yes()],
                                                  env=self.custom_global_env, **kwargs)
            else:
                result = super(Shell, self).run(command, pty=pty, echo_stdin=True,warn=True, watchers=[say_yes()],
                                                env=self.custom_global_env, **kwargs)
            exited, stdout, stderr = result.exited, result.stdout, result.stderr
            if result.failed:
                message = '[%s@%s]# %s\n[ERROR] %s' % (self.user, self.host, command, stdout + stderr)
                error_logger.error(message)
            else:
                message = '[%s@%s]# %s\n%s' % (self.user, self.host, command, stdout)
            if write:
                with open(write, 'a') as f:
                    f.write(message)
            elif ws and webuser:
                message_in = '[%s@%s]# %s' % (self.user, self.host, command)
                websocket = Tailf()
                websocket.send_message(webuser, message_in)
                for m in stdout.split('\n'):
                    websocket.send_message(webuser, m)
            return result
        except Exception as e:
            message = '[%s@%s]%s' % (self.user, self.host, e)
            error_logger.error(message)
            message = '[%s@%s]# %s\n[ERROR] %s' % (self.user, self.host, command, str(e))
            if write:
                with open(write, 'a') as f:
                    f.write(message)
            elif ws and webuser:
                message_in = '[%s@%s]# %s' % (self.user, self.host, command)
                message_out = '[ERROR] %s' % (str(e))
                Tailf.send_message(webuser, message_in)
                for m in message_out.split('\n'):
                    Tailf.send_message(webuser, m)
            result = Result(exited=-1, stderr=message, stdout=message)
            return result

    def local(self, command, write=None, ws=False, webuser=None, **kwargs):
        return self.run(command, run_mode=self.run_mode_local, write=write, ws=ws, webuser=webuser, **kwargs)

    def get(self, remote=None, local=None, write=None, ws=False, webuser=None):
        return self.sync(wtype='get', remote=remote, local=local, write=write, ws=ws, webuser=webuser)

    def put(self, local, remote=None, write=None, ws=False, webuser=None):
        return self.sync(wtype='put', local=local, remote=remote, write=write, ws=ws, webuser=webuser)

    def sync(self, wtype, local=None, remote=None, write=None, ws=False, webuser=None):
        try:
            if wtype == 'put':
                result = super(Shell, self).put(local, remote=remote)
                message = '[%s@%s]# [上传文件]\n[INFO]local:%s to [%s]:%s\n' % (
                            self.user, self.host, local, result.connection.host, remote)
                info_logger.info(message)
                if write:
                    with open(write, 'a') as f:
                        f.write(message)
                elif ws and webuser:
                    Tailf.send_message(webuser,message)
            else:
                result = super(Shell, self).get(remote, local=local)
                message = '[%s@%s]# [下载文件]\n[INFO] [%s]:%s  to local:%s\n' % (
                            self.user, self.host, result.connection.host, remote, local)
                info_logger.info(message)
                if write:
                    with open(write, 'a') as f:
                        f.write(message)
                elif ws and webuser:
                    Tailf.send_message(webuser,message)
            return result
        except Exception as e:
            if wtype == 'put':
                message = '[%s@%s]# [上传文件]\n[ERROR][目标目录:%s][%s]\n' % (self.user, self.host, remote, str(e))
                error_logger.info(message)
                if write:
                    with open(write, 'a') as f:
                        f.write(message)
                elif ws and webuser:
                    Tailf.send_message(webuser,message)
            else:
                message = '[%s@%s]# [下载文件]\n[ERROR][目标目录:%s][%s]\n' % (self.user, self.host, remote, str(e))
                error_logger.info(message)
                if write:
                    with open(write, 'a') as f:
                        f.write(message)
                elif ws and webuser:
                    Tailf.send_message(webuser,message)
