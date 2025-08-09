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
class TaskCreateView(MyLoginRequiredMixin,CreateView):
    model = Task 
    #form_class = TaskForm
    fields = ['author','title']
    success_url = '/todo/task/'
    # template_name = 'todo/task.html'
    
    def form_valid(self,form):
        instance = form.save(commit=False) 
        form.instance.author.user = self.request.user
        instance.save()
        return super().form_valid(form)
    
class TaskListView(MyLoginRequiredMixin,ListView):
    model = Task
    template_name = 'todo/task.html'
    success_url = '/todo/task/'
    context_object_name = 'tasks'
    paginate_by = 50
    ordering = '-created_date' 
      
    def get_queryset(self):
        queryset = super().get_queryset()
        current_user = self.request.user
        queryset = queryset.filter(author__user=current_user)
        return queryset

class TaskEditView(MyLoginRequiredMixin,UpdateView):
    model = Task
    fields = ['title']
    success_url = '/todo/task/'
    
    def form_valid(self,form):
        instance = form.save(commit=False) 
        instance.author.user = self.request.user
        instance.save()
        return super().form_valid(form)
    
class TaskDeleteView(MyLoginRequiredMixin,DeleteView):
    model = Task
    success_url = '/todo/task/'

class TaskCompleteView(MyLoginRequiredMixin,UpdateView):
    model = Task
    fields = []
    success_url = '/todo/task/'
    
    def form_valid(self,form):
        instance = form.save(commit=False) 
        if instance.status == False:
           instance.status = True
        else:
          instance.status = False  
        instance.save()
        return super().form_valid(form)