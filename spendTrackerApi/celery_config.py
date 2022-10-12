import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "spendTrackerApi.settings")

app = Celery("spendTrackerApi")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.beat_schedule = {
    "delay-every-15-min": {
        "task": "api_trip.tasks.delay_trip",
        "schedule": crontab(minute="*/15"),
    }
}
# Load task modules from all registered Django apps.
app.autodiscover_tasks()
