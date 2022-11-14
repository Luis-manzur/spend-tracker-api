import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "spendTrackerApi.settings")

app = Celery("spendTrackerApi")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.beat_schedule = {
    "every-day": {
        "task": "transactions.tasks.apply_monthly_bills",
        "schedule": crontab(minute=0, hour="*/24"),
    }
}
# Load task modules from all registered Django apps.
app.autodiscover_tasks()
