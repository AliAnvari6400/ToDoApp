from django.urls import path,include
from .views import RegistrationApiView,CustomTokenObtainPairView,CustomDiscardAuthtoken,ChangepasswordAPIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,TokenVerifyView)

#app_name = 'api-v1'

urlpatterns = [
    
    # registration:
    path('registration/', RegistrationApiView.as_view(), name='registration'),
    
    # login & logout by token:
    path('token/login/',ObtainAuthToken.as_view(), name='token-login'),
    path('token/logout/',CustomDiscardAuthtoken.as_view(), name='token-logout'),
    
    # JWT:
    path('jwt/create/', CustomTokenObtainPairView.as_view(), name='jwt-create'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # change password:
    path('change-password/', ChangepasswordAPIView.as_view(), name='change-password'),
       
]


