import json

import redis

from rest_framework.response import Response
import traceback

from shixun.settings import REDIS_IP, REDIS_PORT, DB_INDEX


class RDS(object):
    def __init__(self):
        # 不写就是默认本机的
        self.redis = redis.Redis(host=REDIS_IP, port=REDIS_PORT, db=DB_INDEX)

    def left_push(self, key, *value):
        """
        执行lpush 的操作
        从队列左侧插入数据
        """
        try:
            self.redis.lpush(key, *value)
        except:
            error = traceback.format_exc()
            print('Alipay error:{}'.format(error))
            return error

    def right_push(self, key, *value):
        """
        从右侧插入
        """
        try:
            self.redis.rpush(key, *value)
        except:
            error = traceback.format_exc()
            print('Alipay error:{}'.format(error))
            return error

    def right_pop(self, key):
        """右侧弹出数据"""
        try:
            value = self.redis.rpop(key)
            if value:
                value = value.decode('utf-8')
                return value
            return False
        except:
            error = traceback.format_exc()
            print('Alipay error:{}'.format(error))
            return error

    def left_pop(self, key):
        """右侧弹出数据"""
        try:
            value = self.redis.lpop(key)
            if value:
                value = value.decode('utf-8')
                return value
            return False
        except:
            error = traceback.format_exc()
            print('Alipay error:{}'.format(error))
            return error

    def get_list(self, key):
        """
        获取队列数据
        """
        try:
            value = self.redis.lrange(key, 0, -1)
            return value
        except:
            error = traceback.format_exc()
            print(error)
            return []

    # 添加多个
    def set_hash(self, name, key, value):
        try:
            self.redis.hmset(name, mapping={key: value})
            return True
        except:
            error = traceback.format_exc()
            print('set_hash', error)
            return False

    # 查询全部hash
    def get_hash(self, name):
        result = self.redis.hgetall(name)
        return result

    def set_rds(self, name, key, value):
        self.redis.hset(name, key, value)

    def get_rds(self, name, key):
        return self.redis.hget(name, key)

    # 删除hash
    def del_hash(self, name, key):
        try:
            self.redis.hdel(name, key)
            return True
        except:
            error = traceback.format_exc()
            print('del_hash', error)
            return False

    def sadd_set(self, name, values):
        try:
            self.redis.sadd(name, values)
            return True
        except:
            error = traceback.format_exc()
            print('sadd_set', error)
            return False

    def scard_set(self, name):
        result = self.redis.scard(name)
        return result


def get_hash(self, name, key):
    return self.redis.hget(name, key)


def set_hash(self, name, mapping):
    """
    保存hash数据
    """
    try:
        self.redis.hmset(name, mapping=mapping)
        # self.redis.save()
        return True
    except:
        error = traceback.format_exc()
        print('set_hash', error)
        return False


def get_hash_all(self, name):
    """
    获取所有数据
    """
    result = {}
    data = self.redis.hgetall(name)
    for key, value in data.items():
        result.update({json.loads(key): json.loads(value)})
    return result


def del_hash(self, name, key):
    """
    删除key
    """
    self.redis.hdel(name, key)
    # self.redis.save()
