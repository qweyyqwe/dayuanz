import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer

CONN_LIST = []


class ChatConsumer(WebsocketConsumer):
    def websocket_connect(self, message):
        print("开始链接...")

        # 有客户端来向后端发送websocket连接的请求时，自动触发。
        # 服务端允许和客户端创建连接（握手）。
        self.accept()

        CONN_LIST.append(self)

    def websocket_receive(self, message):
        print('22222222', message)
        data = json.loads(message.get('text', '{}'))
        chat_type = data.get('chat_type')
        chat_id = data.get('chat_id')
        chat_content = data.get('message')
        if chat_type == 'add_chat':
            async_to_sync(self.channel_layer.group_add)(chat_id, self.channel_name)
        else:
            async_to_sync(self.channel_layer.group_send)(chat_id, {"type": 'chat.message', 'message': message})

    def chat_message(self, event):
        self.send(event['message']['text'])

    # def websocket_receive(self, message):
    #     # 浏览器基于websocket向后端发送数据，自动触发接收消息。
    #     print('接受的消息', message)
    #     text = message['text']  # {'type': 'websocket.receive', 'text': '阿斯蒂芬'}
    #     print("接收到消息-->", text)
    #     res = {'result': 'ok'}
    #     for conn in CONN_LIST:
    #         conn.send(json.dumps(res))

    def websocket_disconnect(self, message):
        CONN_LIST.remove(self)
        raise StopConsumer()
