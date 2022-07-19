# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : teacher_rabbit_product.py.py
# @Software: PyCharm


"""
生产者消费队列
"""
from multiprocessing import Process
import threading
import pika
import time


class PublishClass(object):
    """单例模式用来少创建连接"""
    # 加锁，防止并发较高时，同时创建对象，导致创建多个对象
    _singleton_lock = threading.Lock()

    def __init__(self, user, password, ip, port, exchange='', exchange_type='', queue_name='task_queue'):
        self.exchange = exchange
        self.exchange_type = exchange_type
        self.queue_name = queue_name
        """__init__在new出来对象后实例化对象"""
        self.credentials = pika.PlainCredentials(user, password)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=ip, port=port, credentials=self.credentials))
        self.channel = self.connection.channel()
        # 创建一个指定名称的交换机，并指定类型为fanout，用于将接收到的消息广播到所有queue中
        self.channel.queue_declare(queue=queue_name)


    def callback(self, ch, method, properties, body):
        print(" [x] %r" % body)

    def connection_close(self):
        """关闭连接"""
        self.connection.close()
        print('>>>>>>>>>>>关闭连接')

    def consuming_start(self):
        """等待消息"""
        self.channel.start_consuming()
        print('>>>>>>>>>>>等待消息')

    def this_publisher(self, message):
        # 3. 创建队列，queue_declare可以使用任意次数，
        # 如果指定的queue不存在，则会创建一个queue，如果已经存在，
        # 则不会做其他动作，官方推荐，每次使用时都可以加上这句
        """发布者
        queue_name：队列名称
        """
        self.channel.basic_publish(exchange=self.exchange, routing_key=self.queue_name, body=message)
        print(" [x] Sent %r" % message)
        self.connection_close()





