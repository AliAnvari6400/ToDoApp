from celery import shared_task
import time
from .models import Task
from rest_framework.test import APIClient


# For Test:
# -------------------------------
@shared_task
def add(x, y):
    time.sleep(10)
    return x + y


@shared_task
def test():
    print("ok")


# --------------------------------


# delete tasks(status=True):
@shared_task
def task_delete():
    Task.objects.filter(status=True).delete()


# Update Weather:
@shared_task
def update_weather():
    url = "http://todoapp:8000/todo/api/v1/weather/"
    api_client = APIClient()
    api_client.get(url)
