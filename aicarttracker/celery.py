import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aicarttracker.settings')

app = Celery('aicarttracker')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()