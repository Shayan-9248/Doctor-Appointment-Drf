import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# app.config_from_object('proj.celeryconfig')
# app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.broker_url = "amqp://guest:guest@localhost:5672/"
app.conf.result_backend = "rpc://"
app.conf.result_serializer = "json"
app.conf.task_serializer = "json"
app.conf.accept_content = ["json", "pickle"]
# app.conf.result_expires = timedelta(days=1)
# app.conf.task_always_eager = False
# app.conf.worker_prefetch_multiplier = 1
