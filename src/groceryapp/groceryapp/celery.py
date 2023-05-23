import os

from celery import Celery
#run celery
# celery -A groceryapp worker --beat --scheduler django --loglevel=info
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'groceryapp.settings')


app=Celery('groceryapp')

app.config_from_object('django.conf:settings',namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule={
    "compute_score_every_60":{
        "task":"grocery_score_change_task",
        "schedule":60,
    }
}
