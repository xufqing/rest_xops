# @Time    : 2019/3/21 14:35
# @Author  : xufqing

from channels.generic.websocket import AsyncWebsocketConsumer
import utils.globalvar as gl

class ConsoleMsgConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.channel_layer.group_add(
            self.scope['user'].username,
            self.channel_name,
        )
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        await self.channel_layer.group_send(
            self.scope['user'].username,
            {
                'type': 'user.message',
                'message': text_data,
            }
        )

    async def disconnect(self, code):
        # 关闭死循环读取日志
        webuser = self.scope['user'].username
        if hasattr(gl,'_global_dict'):
            deploy_key = 'deploy_' + str(webuser)
            tail_key = 'tail_' + str(webuser)
            if deploy_key in gl._global_dict.keys():
                gl.set_value(deploy_key, True)
            elif tail_key in gl._global_dict.keys():
                gl.set_value(tail_key, True)

        await self.channel_layer.group_discard(
            webuser,
            self.channel_name
        )

    async def user_message(self, event):
        await self.send(event['message'])