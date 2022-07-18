# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : code.py
# @Software: PyCharm


import datetime
import random

from utils.redis_cache import mredis


def uniqueness_code(id):
    code = str(datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(id) + str(random.randint(1000, 9999)))
    mredis.setex_str("code_" + str(id), 60*10, code)
    return code
