# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : producer.py
# @Software: PyCharm


"""
生产者消费队列
"""

import pika
import json

credentials = pika.PlainCredentials('admin', '123456')  # mq用户名和密码,用于认证
# 虚拟队列需要指定参数virtual_host，如果是默认的可以不填
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='192.168.10.8', port=5672, virtual_host='/', credentials=credentials))
channel = connection.channel()
# 3. 创建队列，queue_declare可以使用任意次数，
# 如果指定的queue不存在，则会创建一个queue，如果已经存在，
# 则不会做其他动作，官方推荐，每次使用时都可以加上这句
channel.queue_declare(queue='task_queue')

message = 'Hello World! 2222'
channel.basic_publish(
    exchange='',
    routing_key='task_queue',
    body=message,
    # delivery_mode=2可以指定此条消息持久化，防止RabbitMQ服务挂掉之后消息丢失
    # 但是此属性设置并不能百分百保证消息真的被持久化，因为RabbitMQ挂掉的时候
    # 它可能还保存在缓存中，没来得及同步到磁盘中
    # properties=pika.BasicProperties(delivery_mode=2)
)
print(" [x] Sent %r" % message)
connection.close()


