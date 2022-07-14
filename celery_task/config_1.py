BROKER_URL = 'redis://121.36.69.18/11'
CELERY_RESULT_BACKEND = 'redis://121.36.69.18/12'
# 时区
CELERY_TIMEZONE = 'Asia/Shanghai'

# 导入指定的任务模块
CELERY_IMPORTS = (
    'celery_task.tasks',
)