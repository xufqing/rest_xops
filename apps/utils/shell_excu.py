# @Time    : 2019/3/7 16:19
# @Author  : xufqing
from fabric2 import Connection
from invoke import Responder, Result
from utils.websocket_tail import Tailf
from io import StringIO
import logging, os
from cmdb.models import DeviceInfo,ConnectionInfo

error_logger = logging.getLogger('error')
info_logger = logging.getLogger('info')

def say_yes():
    return Responder(
        pattern=r'yes/no',
        response='yes\n',
    )

def connect_init(id):
    device_info = DeviceInfo.objects.filter(id=int(id)).values()
    host = device_info[0]['hostname']
    auth_type = device_info[0]['auth_type']
    connect_info = ConnectionInfo.objects.filter(hostname=host, auth_type=auth_type).values()
    user = connect_info[0]['username']
    passwd = connect_info[0]['password']
    port = connect_info[0]['port']
    auth_info = '{user}@{host}:{port}'.format(user=user, host=host, port=port)
    auth_key = {auth_type: passwd}
    connect = Shell(auth_info, connect_timeout=5, connect_kwargs=auth_key)
    return connect

class Shell(Connection):
    run_mode_remote = 'remote'
    run_mode_local = 'local'
    custom_global_env = {}

    def init_env(self, **kwargs):
        self.custom_global_env = kwargs['env']

    def run(self, command, run_mode=run_mode_remote, write=None, pty=False, webuser=None, **kwargs):
        try:
            stream_out = None
            stream_err = None
            if write:
                io_dict = {}
                file_name = os.path.basename(write)
                io = os.path.splitext(file_name)[0]
                stream_out = io_dict[io + '_out'] = StringIO()
                stream_err = io_dict[io + '_err'] = StringIO()
                message = '[%s@%s]# %s\n' % (self.user, self.host, command)
                file = open(write, 'a')
                #file.write(message)
                stream_out = stream_err = file
                stream_out.write(message)
            if run_mode == self.run_mode_local:
                result = super(Shell, self).local(command, pty=pty, warn=True, out_stream=stream_out, err_stream=stream_err,
                                                  watchers=[say_yes()],
                                                  env=self.custom_global_env, **kwargs)
            else:
                result = super(Shell, self).run(command, pty=pty, warn=True, out_stream=stream_out, err_stream=stream_err,
                                                watchers=[say_yes()],
                                                env=self.custom_global_env, **kwargs)
            exited, stdout, stderr = result.exited, result.stdout, result.stderr
            if result.failed:
                message = '[%s@%s]# %s\n[ERROR] %s' % (self.user, self.host, command, stdout + stdout)
                error_logger.error(message)
            if webuser:
                message_in = '[%s@%s]# %s' % (self.user, self.host, command)
                websocket = Tailf()
                websocket.send_message(webuser, message_in)
                message_out = stdout + stderr
                for m in message_out.split('\n'):
                    websocket.send_message(webuser, m)
            return result
        except Exception as e:
            message = '[%s@%s]%s' % (self.user, self.host, e)
            error_logger.error(message)
            message = '[%s@%s]# %s\n[ERROR] %s' % (self.user, self.host, command, str(e))
            if write:
                with open(write, 'a') as f:
                    f.write(message)
            elif webuser:
                message_in = '[%s@%s]# %s' % (self.user, self.host, command)
                message_out = '[ERROR] %s' % (str(e))
                Tailf.send_message(webuser, message_in)
                for m in message_out.split('\n'):
                    Tailf.send_message(webuser, m)
            result = Result(exited=-1, stderr=message, stdout=message)
            return result

    def local(self, command, write=None, webuser=None, **kwargs):
        return self.run(command, run_mode=self.run_mode_local, write=write, webuser=webuser, **kwargs)

    def get(self, remote=None, local=None, write=None, webuser=None):
        return self.sync(wtype='get', remote=remote, local=local, write=write, webuser=webuser)

    def put(self, local, remote=None, write=None, webuser=None):
        return self.sync(wtype='put', local=local, remote=remote, write=write, webuser=webuser)

    def sync(self, wtype, local=None, remote=None, write=None, webuser=None):
        try:
            if wtype == 'put':
                result = super(Shell, self).put(local, remote=remote)
                message = '[%s@%s]# [上传文件]\n[INFO] 本地:%s 上传到 [%s]:%s\n' % (
                            self.user, self.host, local, result.connection.host, remote)
                info_logger.info(message)
                if write:
                    with open(write, 'a') as f:
                        f.write(message)
                elif webuser:
                    Tailf.send_message(webuser,message)
            else:
                result = super(Shell, self).get(remote, local=local)
                message = '[%s@%s]# [下载文件]\n[INFO] [%s]:%s 下载到 本地:%s\n' % (
                            self.user, self.host, result.connection.host, remote, local)
                info_logger.info(message)
                if write:
                    with open(write, 'a') as f:
                        f.write(message)
                elif webuser:
                    Tailf.send_message(webuser,message)
            return result
        except Exception as e:
            if wtype == 'put':
                message = '[%s@%s]# [上传文件]\n[ERROR] [目标目录:%s][%s]\n' % (self.user, self.host, remote, str(e))
                error_logger.info(message)
                if write:
                    with open(write, 'a') as f:
                        f.write(message)
                elif webuser:
                    Tailf.send_message(webuser,message)
            else:
                message = '[%s@%s]# [下载文件]\n[ERROR] [目标目录:%s][%s]\n' % (self.user, self.host, remote, str(e))
                error_logger.info(message)
                if write:
                    with open(write, 'a') as f:
                        f.write(message)
                elif webuser:
                    Tailf.send_message(webuser,message)
