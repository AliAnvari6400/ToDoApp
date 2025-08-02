from django.views.generic import CreateView,ListView,UpdateView,DeleteView
from .models import Task
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

# customize LoginRequiredMixin for redirect to login page first
class MyLoginRequiredMixin(LoginRequiredMixin):
    def get_login_url(self):
        return reverse_lazy('accounts:login')


# Create,list,edit,delete and complete view for tasks
class TaskCreateView(MyLoginRequiredMixin,CreateView):
    model = Task
    fields = ['author','title']
    success_url = '/todo/task/'
    
class TaskListView(MyLoginRequiredMixin,ListView):
    model = Task
    paginate_by = 100
    context_object_name = 'tasks'
    
class TaskEditView(MyLoginRequiredMixin,UpdateView):
    model = Task
    fields = ['author','title']
    success_url = '/todo/task/'
    
class TaskDeleteView(MyLoginRequiredMixin,DeleteView):
    model = Task
    success_url = '/todo/task/'

class TaskCompleteView(MyLoginRequiredMixin,UpdateView):
    model = Task
    fields = ['status']
    success_url = '/todo/task/'