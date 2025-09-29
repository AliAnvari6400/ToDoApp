from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import get_user_model

User = get_user_model()


# custom UserCreateForm for email as username
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email",)  # Only include email field


# Signup
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("accounts:login")  # Redirect to login page after signup


class MyLoginView(LoginView):
    redirect_authenticated_user = True

    def get_success_url(self):
        next_url = self.get_redirect_url()
        print(next_url)
        if next_url:
            return next_url
        return reverse_lazy("todo:task")
