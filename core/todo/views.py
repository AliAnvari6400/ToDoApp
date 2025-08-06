from django.views.generic import CreateView,ListView,UpdateView,DeleteView
from .models import Task
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import TaskForm

# customize LoginRequiredMixin for redirect to login page first
class MyLoginRequiredMixin(LoginRequiredMixin):
    def get_login_url(self):
        return reverse_lazy('accounts:login')


# Create,list,edit,delete and complete view for tasks
class TaskCombinedView(MyLoginRequiredMixin,CreateView,ListView):
    model = Task
    form_class = TaskForm
    #fields = ['author','title']
    success_url = '/todo/task/'
    template_name = 'todo/task.html'
    ordering = '-created_date'
    context_object_name = 'tasks'
    paginate_by = 10
    
    def form_valid(self,form):
        form.instance.author.user = self.request.user
        return super().form_valid(form)

# class TaskListView(MyLoginRequiredMixin,ListView):
#     model = Task
#     paginate_by = 100
#     context_object_name = 'tasks'
#     template_name = 'todo/task.html'
#     ordering = '-created_date'
    
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