from django.urls import path, include
from django.contrib.auth.views import LogoutView
from .views import SignUpView
from django.views.generic import RedirectView
from .views import MyLoginView

app_name = "accounts"

urlpatterns = [
    path("", RedirectView.as_view(url="todo/task/", query_string=True)),
    # path('',include('django.contrib.auth.urls')),
    path("login/", MyLoginView.as_view(), name="login"),
    path(
        "logout/",
        LogoutView.as_view(next_page="/accounts/login/"),
        name="logout",
    ),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("api/v1/", include("accounts.api.v1.urls")),
]
