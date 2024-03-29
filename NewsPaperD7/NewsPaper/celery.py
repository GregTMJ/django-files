"""
We use Celery to give the server on opportunity to run tasks in parallel without stopping
"""
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'weekly_posts_for_subscribers': {
        'task': 'tasks.weekly_posts',
        'schedule': crontab(),
    },
}
