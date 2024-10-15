# from celery.schedules import crontab
from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')

app = Celery('django_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


"""app.conf.beat_schedule = {
    'run-tests-every-midnight': {
        'task': 'core.tasks.run_tests',
        'schedule': crontab(minute=str(0), hour=str(0)),  # Runs every midnight
    },
}

"""
