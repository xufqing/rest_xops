# @Time    : 2019/3/21 16:16
# @Author  : xufqing
import paramiko, logging, time
from paramiko_expect import SSHClientInteraction
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from utils.common import async
import utils.globalvar as gl

info_logger = logging.getLogger('info')

class Tailf(object):
    @classmethod
    def send_message(self, user, message):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(user, {"type": "user.message", 'message': message})

    def local_tailf(self, logfile, webuser):
        f = open(logfile, 'rt')
        f.seek(0, 0)
        while True:
            line = f.readline()
            if not line:
                is_stop = gl.get_value('deploy_' + str(webuser))
                if is_stop:
                    self.send_message(webuser, '[INFO]文件监视结束..')
                    f.close()
                    break
                else:
                    time.sleep(0.2)
                    continue
            yield line

    def remote_tail(self, host, port, user, passwd, logfile, webuser, filter_text=None):
        # 创建一个可跨文件的全局变量，控制停止
        try:
            self.client = paramiko.SSHClient()
            self.client.load_system_host_keys()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(hostname=host, port=port, username=user, password=passwd)
            interact = SSHClientInteraction(self.client, timeout=10, display=False)
            interact.expect('.*#.*')
            logfile = logfile.strip().replace('&&', '').replace('||', '').replace('|', '')
            self.send_message(webuser, '[INFO][%s@%s]开始监控日志' % (user, host))
            gl._init()
            gl.set_value('tail_' + str(webuser), self.client)
            if filter_text:
                filter_text_re = filter_text.strip().replace('&&', '').replace('||', '').replace('|', '')
                interact.send('tail -f %s|grep --color=never %s' % (logfile, filter_text_re))
            else:
                interact.send('tail -f %s' % (logfile))
            interact.tail(output_callback=lambda m: self.send_message(webuser, m))
        except Exception as e:
            self.send_message(webuser, e)
        finally:
            try:
                self.client.close()
            except Exception as e:
                self.send_message(webuser, e)