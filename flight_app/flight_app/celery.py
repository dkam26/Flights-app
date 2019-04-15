from __future__ import absolute_import
from celery import Celery
import os
from .settings import INSTALLED_APPS
# Setting the Default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE','flight_app.flight_app.settings')
app=Celery('flight_app')


class Config:
    enable_utc = True
    timezone = 'Africa/Nairobi'
# Using a String here means the worker will always find the configuration information
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))