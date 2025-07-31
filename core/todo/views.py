from django.views.generic import CreateView
from .models import Task

# Create your views here.
class TaskCreateView(CreateView):
    model = Task
    fields = ['author','title']
    success_url = '/todo/task/'