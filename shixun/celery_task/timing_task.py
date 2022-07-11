from celery_task import celery_app


@celery_app.task(name='celery_task.timing_task.my_crontab')
def my_crontab(x, y):
    print(x, y)
    return x + y