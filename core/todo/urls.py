from django.urls import path
from .views import TaskCreateView, TaskListView,TaskEditView,TaskDeleteView,TaskCompleteView,TaskCombinedView

app_name = 'todo'

urlpatterns = [
    path('task/', TaskCombinedView.as_view(), name = 'task-create-list'),
    #path('task/', TaskListView.as_view(), name = 'task-list'),
    path('task/<int:pk>/edit/', TaskEditView.as_view(), name = 'task-edit'),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name = 'task-delete'),
    path('task/<int:pk>/complete/', TaskCompleteView.as_view(), name = 'task-complete'),
]