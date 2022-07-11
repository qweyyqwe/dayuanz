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
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_LOG_DIR, 'log-{}.log'.format(time.strftime('%Y-%m-%d'))),
            'when': 'D',
            # 'maxBytes': 1024 * 1024 * 50,  # 日志大小50M
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
            'propagate': False
        },
    },

}
