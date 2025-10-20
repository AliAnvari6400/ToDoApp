from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Task
from accounts.models import Profile
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.urls import reverse_lazy
from .forms import TaskForm
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.http import Http404
import requests
from django.http import JsonResponse

# from django.core.cache import cache
from django.views.decorators.cache import cache_page
from todo.tasks import add
from django.http import HttpResponse


# customize LoginRequiredMixin for redirect to login page first
class MyLoginRequiredMixin(LoginRequiredMixin):
    def get_login_url(self):
        return reverse_lazy("accounts:login")


# Combined CreateView and ListView
class TaskView(MyLoginRequiredMixin, CreateView, ListView):
    model = Task
    template_name = "todo/task.html"
    success_url = "/todo/task/"
    context_object_name = "tasks"
    paginate_by = 50
    form_class = TaskForm

    def get_queryset(self):
        queryset = super().get_queryset()
        current_user = self.request.user
        queryset = queryset.filter(author__user=current_user)
        return queryset.order_by("-created_date")

    def get_initial(self):
        initial = super().get_initial()
        if self.request.user.is_authenticated:
            initial["author"] = Profile.objects.get(user=self.request.user)
        return initial

    def form_valid(self, form):
        self.object = form.save()
        user = self.request.user
        content_type = ContentType.objects.get_for_model(Task)
        view_permission = Permission.objects.get(
            codename="view_task", content_type=content_type
        )
        user.user_permissions.add(view_permission)
        return super().form_valid(form)


class TaskEditView(MyLoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Task
    fields = ["title"]
    success_url = "/todo/task/"
    permission_required = "todo.view_task"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=Profile.objects.get(user=self.request.user))

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        try:
            obj = super().get_object(queryset)
        except Http404:
            # Instead of 404, raise 403 here
            raise PermissionDenied
        return obj


class TaskDeleteView(MyLoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Task
    success_url = "/todo/task/"
    permission_required = "todo.view_task"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=Profile.objects.get(user=self.request.user))

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        try:
            obj = super().get_object(queryset)
        except Http404:
            # Instead of 404, raise 403 here
            raise PermissionDenied
        return obj


class TaskCompleteView(MyLoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Task
    fields = ["status"]
    success_url = "/todo/task/"
    template_name = "todo/task_complete.html"
    permission_required = "todo.view_task"

    def form_valid(self, form):
        instance = form.save(commit=False)
        if instance.status is False:
            instance.status = True
        else:
            instance.status = False
        instance.save()
        return super(TaskCompleteView, self).form_valid(form)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=Profile.objects.get(user=self.request.user))

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        try:
            obj = super().get_object(queryset)
        except Http404:
            # Instead of 404, raise 403 here
            raise PermissionDenied
        return obj


# Test Celery task:
# ---------------------------------
def test(request):
    result = add.delay(3, 3)
    print(result.id)
    return HttpResponse("done")


# ---------------------------------


# Test Redis for cache:
# ---------------------------------
# def weather(request):
#     API_KEY = '6075f690e844e83ffc96d4ddf40c8b18'
#     city = 'Tehran'
#     url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
#     if cache.get('test') is None:
#         response = requests.get(url)
#         cache.set('test',response.json(),30)
#     return JsonResponse(cache.get('test'))


@cache_page(30)
def weather(request):
    API_KEY = (
        "6075f690e844e83ffc96d4ddf40c8b18"  # Replace with your OpenWeather API key
    )
    city = "Tehran"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    return JsonResponse(response.json())


# ---------------------------------


# Weather Show:
class WeatherView(TemplateView):
    template_name = "todo/weather.html"
