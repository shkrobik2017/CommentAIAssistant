from celery import Celery

app_celery = Celery(
    "tasks",
    broker="redis://redis:6379/0"
)


app_celery.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
)

import celery_app.tasks
