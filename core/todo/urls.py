from django.urls import path
from .views import TaskEditView,TaskDeleteView,TaskCompleteView,TaskListView,TaskCreateView

app_name = 'todo'

urlpatterns = [
    path('task/', TaskListView.as_view(), name = 'task-list'),
    path('task/create/', TaskCreateView.as_view(), name = 'task-create'),
    #path('task/', TaskListView.as_view(), name = 'task-list'),
    path('task/<int:pk>/edit/', TaskEditView.as_view(), name = 'task-edit'),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name = 'task-delete'),
    path('task/<int:pk>/complete/', TaskCompleteView.as_view(), name = 'task-complete'),
]