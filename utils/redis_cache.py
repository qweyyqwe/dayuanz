# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : redis_cache.py
# @Software: PyCharm


import redis


class Mredis:
    def __init__(self) -> None:
        self.pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=2)
        self.conn = redis.Redis(connection_pool=self.pool)
        # self.cursor = self.conn.cursor()

    # 字符串添加
    # def str_set(self, key, time, value):
    #     self.conn.set(key, time, value)

    # #更新添加
    # def update(self,sql):
    #         self.cursor.execute(sql)
    #         self.conn.commit()
    #         return self.cursor.lastrowid

    def setex_str(self, key, time, value):
        self.conn.setex(key, time, value)

    # 字条串读取
    def str_get(self, key):
        return self.conn.get(key)

    # 数据放入列表 (放入队列)
    def l_push(self, key, value):
        self.conn.lpush(key, value)

    # 优先加入
    def r_push(self, key, value):
        self.conn.rpush(key, value)

    # key中的元素个数
    def t_len(self, key):
        return self.conn.llen(key)

    def r_pop(self, key):
        return self.conn.rpop(key)

    # 获取单个
    def hash_one(self, gkey, key):
        return self.conn.hget(gkey, key)




mredis = Mredis()
