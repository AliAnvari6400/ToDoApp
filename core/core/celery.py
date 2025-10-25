import os
from celery import Celery

# Set default Django settings module for 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Automatically discover tasks.py modules in Django apps
app.autodiscover_tasks()


# For Test Beat:
# ---------------------------------
app.conf.beat_schedule = {
    "run-every-minute": {
        "task": "todo.tasks.test",  # path to task
        "schedule": 5,
        # Or use 'schedule': 60.0 for seconds (every 60 seconds)
    },
}
app.conf.timezone = "UTC"
# ---------------------------------
