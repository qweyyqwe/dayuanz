# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : aaa.py
# @Software: PyCharm

# import json
# from channels.generic.websocket import WebsocketConsumer
# from channels.exceptions import StopConsumer
# from asgiref.sync import async_to_sync
# CONN_LIST = []
#
# class ChatConsumer(WebsocketConsumer):
#     def websocket_connect(self, message):
#         # 接收这个客户端的连接
#         self.accept()
#         print("1111111111",message)
#         CONN_LIST.append(self)
#         # 将这个客户端的连接对象加入到某个地方（内存 or redis）1314 是群号这里写死了
#         # async_to_sync(self.channel_layer.group_add)('1314', self.channel_name)
#
#     def websocket_receive(self, message):
#         # 通知组内的所有客户端，执行 xx_oo 方法，在此方法中自己可以去定义任意的功能。
#         print("222222222222",message)
#         data = json.loads(message.get('text','{}'))
#         chat_type = data.get('chat_type')
#         chat_id = data.get('chat_id')
#         chat_content = data.get('message')
#         #创建聊天群组
#         print("chat_type>>>>>",type(chat_type))
#         if chat_type == "add_chat":
#             async_to_sync(self.channel_layer.group_add)(chat_id, self.channel_name)
#         else:
#             async_to_sync(self.channel_layer.group_send)(chat_id, {'type':"chat.message","message":message})
#         # async_to_sync(self.channel_layer.group_send)('1314', {"type": "xx.oo", 'message': message})
#         # 这个方法对应上面的type，意为向1314组中的所有对象发送信息
#
#     def chat_message(self, event):
#         print("hahahahahaa")
#         text = event['message']['text']
#         self.send(text)
#
#     def websocket_disconnect(self, message):
#         print("3333333",message)
#         data = json.loads(message['text'])
#         chat_id = data.get('chat_id')
#         # 断开链接要将这个对象从 channel_layer 中移除
#         async_to_sync(self.channel_layer.group_discard)(chat_id,self.channel_name)
#         raise StopConsumer()


# 1877931656059988
# print(len('1877931656059988'[:-15]))

# a = '哇哇哇'
#
# print(type(a))

# a = {'img_list': ['http://rd4zpkzab.hd-bkt.clouddn.com//upload_pic_可利4.png', 'http://rd4zpkzab.hd-bkt.clouddn.com//upload_pic_可利3.png'], 'form': {'name': '109', 'desc': '12', 'image': '', 'price': '3', 'count': '1'}}
#
# print(a['form'].get('name'))


# import datetime
# def get_now_time():
#     """获取当前时间"""
#     from django.utils import timezone
#     import pytz
#     tz = pytz.timezone('Asia/Shanghai')
#     # 返回时间格式的字符串
#     now_time = timezone.now().astimezone(tz=tz)
#     now_time_str = now_time.strftime("%Y.%m.%d %H:%M:%S")
#
#     # 返回datetime格式的时间
#     now_time = timezone.now().astimezone(tz=tz).strftime("%Y-%m-%d %H:%M:%S")
#     now = datetime.datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S')
#     print(now_time)
#     print(now)


# # 冒泡排序核心代码，
# list1 = [3, 1, 92, 43, 2, 71, 32, 12]
# for j in range(len(list1) - 1):
#     for k in range(len(list1) - 1):
#         # print('kkkkkkkkkk', k)
#         if list1[k] > list1[k + 1]:     # 如果list1[k]小于list1[k+1]
#             # print('判断1111111', list1[k], list1[k+1])
#             t = list1[k]
#             # print('t>><<<<<<<<<<', t)
#             list1[k] = list1[k + 1]
#             list1[k + 1] = t
#             # print('最后t——', t)
# print(list1)


# def bubble_sort(blist):
#     count = len(blist)
#     for i in range(0, count):
#         for j in range(i + 1, count):
#             if blist[i] > blist[j]:
#                 blist[i], blist[j] = blist[j], blist[i]
#     return blist
#
# blist = bubble_sort([3, 1, 92, 43, 2, 71, 32, 12])
# print(blist)


# # 选择
# def selectionSort(arr):
#     for i in range(len(arr) - 1):
#         # 记录最小数的索引
#         minIndex = i
#         for j in range(i + 1, len(arr)):
#             if arr[j] < arr[minIndex]:
#                 minIndex = j
#         # i 不是最小数时，将 i 和最小数进行交换
#         if i != minIndex:
#             arr[i], arr[minIndex] = arr[minIndex], arr[i]
#     return arr
#
# xuanze = selectionSort([3, 1, 92, 43, 2, 71, 32, 12])
# print(xuanze)


# # {"code":200,"data":[{"id":33,"name":"12312","card_id":"123123123123456","bank_card_id":"1231231231","password":"231233","phone":"15555555555","user":10}]}
# data = [{"id": 33, "name": "12312", "card_id": "123123123123456", "bank_card_id": "1231231231", "password": "231233",
#          "phone": "15555555555", "user": 10}]
# lis = [i['name'] for i in data]
# print(lis)

# import re
#
# p = re.compile('blue|white|red')
#
# print(type(p.subn(' colour', 'blue socks and red shoes')))
#
# # colour socks and colourshoes
#
# print(p.subn('colour', 'blue socks and red shoes', count=1))
#
# # colour socks and redshoes

