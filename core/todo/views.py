from django.views.generic import CreateView,ListView,UpdateView,DeleteView
from .models import Task

# Create your views here.
class TaskCreateView(CreateView):
    model = Task
    fields = ['author','title']
    success_url = '/todo/task/'
    
class TaskListView(ListView):
    model = Task
    paginate_by = 100
    context_object_name = 'tasks'
    
class TaskEditView(UpdateView):
    model = Task
    fields = ['author','title']
    success_url = '/todo/task/'
    
class TaskDeleteView(DeleteView):
    model = Task
    success_url = '/todo/task/'

class TaskCompleteView(UpdateView):
    model = Task
    fields = ['status']
    success_url = '/todo/task/'