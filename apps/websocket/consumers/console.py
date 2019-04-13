# @Time    : 2019/3/21 14:35
# @Author  : xufqing

from channels.generic.websocket import AsyncWebsocketConsumer
from common.custom import RedisObj

class ConsoleMsgConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_anonymous:
            await self.close()
        else:
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
        # 关闭远程tail
        webuser = self.scope['user'].username
        redis = RedisObj()
        remote_tail_is_stop = redis.get('remote_tail_' + str(webuser))
        if remote_tail_is_stop == '0':
            redis.set('remote_tail_' + str(webuser), '1')

        await self.channel_layer.group_discard(
            webuser,
            self.channel_name
        )

    async def user_message(self, event):
        await self.send(event['message'])
