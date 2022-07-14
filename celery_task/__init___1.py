from datetime import timedelta

from celery import Celery
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shixun.settings")
django.setup()
celery_app = Celery('mycelery')
celery_app.config_from_object('celery_task.config')
celery_app.autodiscover_tasks(['celery_task.timing_task'])

celery_app.conf.update(
    CELERYBEAT_SCHEDULE={
        # 'sum-task': {
        #     'task': 'celery_task.timing_task.my_crontab',
        #     'schedule': timedelta(seconds=16),
        #     'args': (5, 6)
        # },
        'sum-task': {
            'task': 'celery_tasks.timing_task.every_bank_loan',
            'schedule': timedelta(seconds=86400),
        },
    }
)

# celery_app.conf.update(
#     CELERYBEAT_SCHEDULE={
#         'sum-task': {
#             'task': 'celery_task.timing_task.my_times3',
#             'schedule': timedelta(seconds=16000000),
#         },
#     }
# )


# celery_app.conf.update(
#     CELERYBEAT_SCHEDULE={
#         'sum-task': {
#             'task': 'celery_task.timing_task.my_times4',
#             'schedule': timedelta(seconds=16000000),
#         },
#     }
# )
