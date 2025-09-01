from django.urls import path
from .views import tasklist

app_name = 'api-v1'

urlpatterns = [
    path('task/', tasklist ,name= 'task-list'),
]