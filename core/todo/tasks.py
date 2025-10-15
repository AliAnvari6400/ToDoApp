from celery import shared_task
import time
from .models import Task

# For Test:
# -------------------------------
@shared_task
def add(x, y):
    time.sleep(10)
    return x + y

@shared_task
def test():
    print('ok')
# --------------------------------

# delete tasks(status=True):
@shared_task
def task_delete():
    Task.objects.filter(status=True).delete()

