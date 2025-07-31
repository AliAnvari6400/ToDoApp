from django.urls import path
from .views import TaskCreateView

app_name = 'todo'

urlpatterns = [
    path('task/create/', TaskCreateView.as_view(), name = 'task_create'),
]