# @Time    : 2019/3/21 16:16
# @Author  : xufqing
import paramiko, logging
from paramiko_expect import SSHClientInteraction
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from utils.common import async
import utils.globalvar as gl

info_logger = logging.getLogger('info')

class Tailf(object):

    def send_message(self, user, message):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(user, {"type": "user.message", 'message': message})

    def read_file(self,logfile, webuser):
        try:
            with open(logfile, 'rt') as f:
                for line in f:
                    self.send_message(webuser, line)
        except Exception as e:
            self.send_message(webuser, e)
    @async
    def local_tail(self, logfile, webuser):
        # 创建一个可跨文件的全局变量，以便控制死循环
        gl._init()
        gl.set_value('deploy_'+ str(webuser), False)
        try:
            with open(logfile, 'rt') as f:
                f.seek(0, 0)
                while True:
                    is_stop = gl.get_value('deploy_' + str(webuser))
                    line = f.readline()
                    if line:
                        self.send_message(webuser, line)
                    elif is_stop:
                        self.send_message(webuser, '[INFO]文件监视结束..')
                        break
        except Exception as e:
            self.send_message(webuser, e)

    def remote_tail(self, host, port, user, passwd, logfile, webuser, filter_text):
        # 创建一个可跨文件的全局变量，控制停止
        gl._init()
        gl.set_value('tail_' + str(webuser), False)
        try:
            self.client = paramiko.SSHClient()
            self.client.load_system_host_keys()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(hostname=host, port=port, username=user, password=passwd)
            interact = SSHClientInteraction(self.client, timeout=10, display=False)
            interact.expect('.*#.*')
            logfile = logfile.strip().replace('&&', '').replace('||', '').replace('|', '')
            self.send_message(webuser, '[INFO][%s@%s]开始监控日志' % (user, host))
            if filter_text:
                filter_text_re = filter_text.strip().replace('&&', '').replace('||', '').replace('|', '')
                interact.send('tail -f %s|grep --color=never %s' % (logfile, filter_text_re))
            else:
                interact.send('tail -f %s' % (logfile))
            interact.tail(output_callback=lambda m: self.send_message(webuser, m),stop_callback=lambda x: gl.get_value('tail_' + str(webuser)), timeout=600)
        except Exception as e:
            self.send_message(webuser, e)
        finally:
            try:
                self.client.close()
            except Exception as e:
                self.send_message(webuser, e)