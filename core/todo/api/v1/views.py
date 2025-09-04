from .serializers import TaskSerializer
from ...models import Task
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .paginations import DefaultPagination

class TaskModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,IsOwnerOrReadOnly]
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author','status']  
    search_fields = ['title']      
    ordering_fields = ['published_date']
    
    pagination_class = DefaultPagination
    
    def get_queryset(self):   # list items for only owner
        return Task.objects.filter(author__user=self.request.user)