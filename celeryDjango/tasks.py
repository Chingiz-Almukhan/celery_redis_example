import requests
from celery import shared_task
from django.core.mail import send_mail

from celeryProject.celery import app
from .models import Contact

from .service import send, save_categories, save_all_emails


@app.task()
def write_file(email):
    send(email)
    return True


@app.task
def get_api():
    response = requests.get('https://api.publicapis.org/categories')
    if response.status_code == 200:
        save_categories(response.json())
        return True
    return False


@app.task()
def write_all_emails():
    counter = 1
    for contact in Contact.objects.all():
        save_all_emails(contact.email, counter)
        counter += 1


@app.task()
def send_beat_email():
    for contact in Contact.objects.all():
        send_mail(
            'test',
            'test 2',
            'testeruly@yandex.kz',
            [contact.email],
            fail_silently=False,
        )


@app.task
def my_task(a, b):
    return a + b


@app.task(bind=True, default_retry_delay=5 * 60)
def my_task_retry(self, x, y):
    try:
        return x + y
    except Exception as e:
        raise self.retry(exc=e, countdown=60)


@shared_task() # sh == app
def my_sh_task(msg):
    return msg + "!!!"


