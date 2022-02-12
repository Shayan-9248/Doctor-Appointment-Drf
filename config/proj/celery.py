import os

from celery import Celery

# os.environ.setdefault('DJANGOSETTINGS_MODULE', 'config..')

app = Celery('config')

app.config_from_object('proj.celeryconfig')
