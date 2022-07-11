# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : log_setting.py
# @Software: PyCharm


"""
log配置
"""
import os
import time

cur_path = os.path.dirname(os.path.realpath(__file__))
BASE_LOG_DIR = os.path.join(os.path.dirname(cur_path), 'log')
if not os.path.exists(BASE_LOG_DIR):
    os.mkdir(BASE_LOG_DIR)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # 设置已存在的logger不失效
    'filters': {},
    'formatters': {
        'standard': {
            'format': '[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d:%(funcName)s]：%(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '[%(asctime)s][%(levelname)s]：%(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_LOG_DIR, 'log-{}.log'.format(time.strftime('%Y-%m-%d'))),
            'maxBytes': 1024 * 1024 * 50,  # 日志大小50M
            'backupCount': 5,
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        'check': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_LOG_DIR, 'check-{}.log'.format(time.strftime('%Y-%m-%d'))),
            'maxBytes': 1024 * 1024 * 50,  # 日志大小50M
            'backupCount': 5,
            'formatter': 'standard',
            'encoding': 'utf-8',
        },

    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False
        },
        'log': {
            'handlers': ['default', 'console'],
            'level': 'INFO',
            'propagate': True
        },
        'check_plaza': {
            'handlers': ['check', 'console'],
            'level': 'INFO',
            'propagate': True
        },
    },

}
