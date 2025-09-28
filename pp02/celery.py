import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pp02.settings')

app = Celery('proj')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()