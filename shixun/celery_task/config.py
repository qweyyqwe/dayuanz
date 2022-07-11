BROKER_URL = 'redis://127.0.0.1/11'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1/12'
# 时区
CELERY_TIMEZONE = 'Asia/Shanghai'

# 导入指定的任务模块
CELERY_IMPORTS = (
    'celery_task.tasks',
)