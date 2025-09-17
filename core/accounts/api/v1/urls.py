from django.urls import path,include
from .views import RegistrationApiView
from rest_framework.authtoken.views import ObtainAuthToken
from .views import CustomDiscardAuthtoken

#app_name = 'api-v1'

urlpatterns = [
    
    # registration:
    path('registration/', RegistrationApiView.as_view(), name='registration'),
    
    # login & logout by token:
    path('token/login/',ObtainAuthToken.as_view(), name='token-login'),
    path('token/logout/',CustomDiscardAuthtoken.as_view(), name='token-logout'),
    
]


