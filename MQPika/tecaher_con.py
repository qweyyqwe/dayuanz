# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : tecaher_con.py
# @Software: PyCharm


import json
import threading
import time
import requests

import pika
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dyz_account.settings")
django.setup()


class Consumer(object):
    """单例模式用来少创建连接"""
    # 加锁，防止并发较高时，同时创建对象，导致创建多个对象
    _singleton_lock = threading.Lock()

    def __init__(self, user, password, ip, port, queue='task_queue'):
        """__init__在new出来对象后实例化对象"""
        self.credentials = pika.PlainCredentials(user, password)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=ip, port=port, credentials=self.credentials))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue)
        print('>>>连接成功')

    def callback(self, ch, method, properties, body):
        # 1、通过orm模型映射
        # 2、直接sql语句，修改数据库
        # 3、通过api接口调用
        print(" [x] %r" % body)
        body = body.decode('utf-8')
        data = json.loads(body)
        url = 'http://127.0.0.1:8000/bank/update_invest_record'
        result = requests.post(url, data)
        print('6666666666', result.json())
        ch.basic_ack(delivery_tag=method.delivery_tag)


    def connection_close(self):
        """关闭连接"""
        self.connection.close()
        print('>>>>>>>>>>>关闭连接')

    def consuming_start(self):
        """等待消息"""
        self.channel.start_consuming()
        print('>>>>>>>>>>>等待消息')

    def this_subscriber(self,  queue_name='task_queue'):
        """
        queue_name：队列名称
        prefetch_count:限制未处理消息的最大值,ack未开启时生效
        """
        # 指定交换机

        print(' [*] Waiting for messages.')
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(
            queue=queue_name, on_message_callback=self.callback)
        self.channel.start_consuming()


if __name__ == '__main__':
    obj1 = Consumer(user='admin', password='admin', ip='47.111.69.97', port=5672)
    obj1.this_subscriber()
