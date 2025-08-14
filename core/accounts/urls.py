from django.urls import path
from django.contrib.auth.views import LoginView,LogoutView
from .views import SignUpView
from django.views.generic import RedirectView

app_name = 'accounts'

urlpatterns = [
    path('',RedirectView.as_view(url='todo/task/', query_string=True)),
    path('login/', LoginView.as_view(redirect_field_name='continue_to'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'), 
]
