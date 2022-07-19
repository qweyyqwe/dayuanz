import threading
import pika
import time


class SingletonClass(object):
    """单例模式用来少创建连接"""
    # 加锁，防止并发较高时，同时创建对象，导致创建多个对象
    _singleton_lock = threading.Lock()

    def __init__(self, user, password, ip, port):
        """__init__在new出来对象后实例化对象"""
        self.credentials = pika.PlainCredentials(user, password)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=ip, port=port, credentials=self.credentials))
        self.channel = self.connection.channel()
        print('>>>连接成功')

    def callback(self, ch, method, properties, body):
        print(" [x] Received %r" % body.decode())
        # 此处以消息中的“.”的数量作为sleep的值，是为了模拟不同消息处理的耗时
        time.sleep(1)
        print(" [x] Done")
        # 手动标记消息已接收并处理完毕，RabbitMQ可以从queue中移除该条消息
        ch.basic_ack(delivery_tag=method.delivery_tag)
        # b = SingletonClass('admin', '123456', '127.0.0.1', 5672)
        # b.this_publisher('7676767676767', queue_name='test1')

    def connection_close(self):
        """关闭连接"""
        self.connection.close()
        print('>>>>>>>>>>>关闭连接')

    def consuming_start(self):
        """等待消息"""
        self.channel.start_consuming()
        print('>>>>>>>>>>>等待消息')

    def this_publisher(self, message, queue_name='task_queue'):
        # 3. 创建队列，queue_declare可以使用任意次数，
        # 如果指定的queue不存在，则会创建一个queue，如果已经存在，
        # 则不会做其他动作，官方推荐，每次使用时都可以加上这句
        """发布者
        queue_name：队列名称
        """
        self.channel.queue_declare(queue='task_queue')

        self.channel.basic_publish(
            exchange='',
            routing_key='task_queue',
            body=message,
            # delivery_mode=2可以指定此条消息持久化，防止RabbitMQ服务挂掉之后消息丢失
            # 但是此属性设置并不能百分百保证消息真的被持久化，因为RabbitMQ挂掉的时候
            # 它可能还保存在缓存中，没来得及同步到磁盘中
            # properties=pika.BasicProperties(delivery_mode=2)
        )
        print(" [x] Sent %r" % message)
        self.connection.close()

    def this_subscriber(self, queue_name='task_queue', prefetch_count=10):
        """
        订阅者
        queue_name：队列名称
        prefetch_count:限制未处理消息的最大值,ack未开启时生效
        """
        self.channel.queue_declare(queue='task_queue')
        print(' [*] Waiting for messages.')
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue='task_queue', on_message_callback=self.callback)

        self.channel.start_consuming()


if __name__ == '__main__':
    obj1 = SingletonClass('admin', 'admin', '47.111.69.97', 5672)
    print(id(obj1))
    # 发布消息
    obj1.this_publisher("123456789")
    # back = SingletonClass()
    # back.this_subscriber()
