from .serializers import TaskSerializer
from ...models import Task
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

class TaskModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    queryset = Task.objects.all()