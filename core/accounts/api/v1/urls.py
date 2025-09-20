from django.urls import path,include
from .views import RegistrationApiView,CustomTokenObtainPairView,CustomDiscardAuthtoken,ChangepasswordAPIView,ProfileAPIView,CustomObtainAuthToken,TestEmailSend
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,TokenVerifyView)

app_name = 'api-v1'

urlpatterns = [
    
    # registration:
    path('registration/', RegistrationApiView.as_view(), name='registration'),
    
    # login & logout by token:
    path('token/login/',CustomObtainAuthToken.as_view(), name='token-login'),
    path('token/logout/',CustomDiscardAuthtoken.as_view(), name='token-logout'),
    
    # JWT:
    path('jwt/create/', CustomTokenObtainPairView.as_view(), name='jwt-create'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # change password:
    path('change-password/', ChangepasswordAPIView.as_view(), name='change-password'),
    
    # profile:
    path('profile/', ProfileAPIView.as_view(), name='profile'),
    
    # activation:
    # path('activation/confirm/',.as_view(), name='activation-confirm'),
    # path('activation/resend/',.as_view(), name='activation-resend'),
    
    # email sending test:
    path('test-email/',TestEmailSend.as_view(), name='test-email'),
       
]


