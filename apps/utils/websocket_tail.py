# @Time    : 2019/3/21 16:16
# @Author  : xufqing
import paramiko, logging, time
from paramiko_expect import SSHClientInteraction
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from common.custom import RedisObj

info_logger = logging.getLogger('info')

class Tailf(object):
    @classmethod
    def send_message(self, user, message):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(user, {"type": "user.message", 'message': message})

    def get_is_stop(self, webuser):
        redis = RedisObj()
        is_stop = redis.get('remote_tail_' + str(webuser))
        return True if is_stop == '1' else False

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
            redis = RedisObj()
            redis.set('remote_tail_' + str(webuser), self.client)
            if filter_text:
                filter_text_re = filter_text.strip().replace('&&', '').replace('||', '').replace('|', '')
                interact.send('tail -f %s|grep --color=never %s' % (logfile, filter_text_re))
            else:
                interact.send('tail -f %s' % (logfile))
            interact.tail(output_callback=lambda m: self.send_message(webuser, m), stop_callback=lambda x: self.get_is_stop(webuser))
        except Exception as e:
            self.send_message(webuser, e)
        finally:
            redis = RedisObj()
            redis.set('remote_tail_' + str(webuser), '1')
            try:
                self.client.close()
            except Exception as e:
                self.send_message(webuser, e)