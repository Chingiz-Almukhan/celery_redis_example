import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celeryProject.settings')

app = Celery('celeryProject', )
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'save-all-emails-every-5-minute': {
        'task': 'celeryDjango.tasks.send_beat_email',
        'schedule': crontab(minute='*/15'),
    },
    'save-all-emails': {
        'task': 'celeryDjango.tasks.write_all_emails',
        'schedule': crontab(minute='*/2'),
    },
    'get_categories_every_one_minutes': {
        'task': 'celeryDjango.tasks.get_api',
        'schedule': crontab(minute='*/1')
    },
}
