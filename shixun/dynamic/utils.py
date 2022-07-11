"""
广场相关方法
"""
import redis

from shixun.redis_utils import RDS


rds = RDS()
dynamic_key = 'dynamic'
checker_key = 'checker'


def add_dynamic_to_redis(dynamic_id):
    """
    添加动态数据到redis队列
    :return:
    """
    add_data_to_queue(dynamic_key, dynamic_id)


def add_user_to_redis(user_id):
    """
    添加审核员到redis数据中
    :param user_id:
    :return:
    """
    add_data_to_queue(checker_key, user_id)


def add_data_to_queue(key, value):
    """
    添加数据到队列中
    :param key:
    :param value:
    :return:
    """
    redis_list = rds.get_list(key)
    redis_list = [i.decode('utf-8') for i in redis_list]
    if value not in redis_list:
        rds.right_push(key, value)

from celery_task.tasks import send_email1
def distribute_dynamic():
    """
    分配  审核 动态
    :return:
    """
    dynamic_id = rds.left_pop(dynamic_key)
    user_id = rds.left_pop(checker_key)
    add_user_to_redis(user_id)
    # TODO 发邮件通知审核人员进行审核  邮件中包含：链接地址
    email = '247304066@qq.com'
    subject = '重置密码'
    # context = {}
    message = "点击'http://localhost:8000/user/pass_code?dynamic_id={}'进行审核".format(dynamic_id)
    from_email = '2457304066@qq.com'
    to_email = ['2457304066@qq.com']
    send_email1.delay(subject, message, from_email, to_email)
    # 成功存入redis,code为key,邮箱为value加过期时间
    res = redis.Redis()
    res.setex(dynamic_id, 36000, email)
    res.close()
