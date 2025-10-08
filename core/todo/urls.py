from django.urls import path, include
from .views import TaskEditView, TaskDeleteView, TaskCompleteView, TaskView

app_name = "todo"

urlpatterns = [
    path("task/", TaskView.as_view(), name="task"),
    path("task/<int:pk>/edit/", TaskEditView.as_view(), name="task-edit"),
    path(
        "task/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"
    ),
    path(
        "task/<int:pk>/complete/",
        TaskCompleteView.as_view(),
        name="task-complete",
    ),
    path("api/v1/", include("todo.api.v1.urls")),
]
