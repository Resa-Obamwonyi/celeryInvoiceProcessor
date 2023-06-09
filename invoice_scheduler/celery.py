from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "invoice_scheduler.settings")

app = Celery("invoice_scheduler")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
    
@app.task(bind=True)
def debug_task(self):
    print('Hello Celery World')
    
app.conf.beat_schedule = {
    # Executes daily at midnight
    'process_invoice-daily': {
        'task': 'process_invoice_task',
        'schedule': crontab(minute=0, hour=0),
    },
}

