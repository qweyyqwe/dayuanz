# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : consumer.py
# @Software: PyCharm


# 消费者
import time

import pika


def main():
    credentials = pika.PlainCredentials('admin', '123456')  # mq用户名和密码,用于认证
    # 虚拟队列需要指定参数virtual_host，如果是默认的可以不填
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='192.168.10.8', port=5672, virtual_host='/', credentials=credentials))
    # 2. 创建一个channel
    channel = connection.channel()
    # 3. 创建队列，queue_declare可以使用任意次数，
    # 如果指定的queue不存在，则会创建一个queue，如果已经存在，
    # 则不会做其他动作，官方推荐，每次使用时都可以加上这句
    channel.queue_declare(queue='task_queue')
    print(' [*] Waiting for messages.')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body.decode())
        # 此处以消息中的“.”的数量作为sleep的值，是为了模拟不同消息处理的耗时
        time.sleep(2)
        print(" [x] Done")
        # 手动标记消息已接收并处理完毕，RabbitMQ可以从queue中移除该条消息
        ch.basic_ack(delivery_tag=method.delivery_tag)

    # prefetch_count表示接收的消息数量，当我接收的消息没有处理完（用basic_ack
    # 标记消息已处理完毕）之前不会再接收新的消息了
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='task_queue', on_message_callback=callback)

    channel.start_consuming()


if __name__ == '__main__':
    main()

