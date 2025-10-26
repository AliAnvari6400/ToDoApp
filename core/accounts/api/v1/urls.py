from django.urls import path
from .views import (
    RegistrationApiView,
    CustomTokenObtainPairView,
    CustomDiscardAuthtoken,
    ChangepasswordAPIView,
    ProfileAPIView,
    CustomObtainAuthToken,
    ActivationApiView,
    ActivationResendApiView,
    ResetPasswordRequestAPIView,
    ResetPasswordConfirmAPIView,
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

app_name = "api-v1"

urlpatterns = [
    # Registration:
    path("registration/", RegistrationApiView.as_view(), name="registration"),
    # Login & Logout by Token:
    path("token/login/", CustomObtainAuthToken.as_view(), name="token-login"),
    path("token/logout/", CustomDiscardAuthtoken.as_view(), name="token-logout"),
    # JWT:
    path("jwt/create/", CustomTokenObtainPairView.as_view(), name="jwt-create"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="token_verify"),
    # Change Password:
    path(
        "change-password/",
        ChangepasswordAPIView.as_view(),
        name="change-password",
    ),
    # profile:
    path("profile/", ProfileAPIView.as_view(), name="profile"),
    # Activation:
    path(
        "activation/confirm/<str:token>",
        ActivationApiView.as_view(),
        name="activation-confirm",
    ),
    path(
        "activation/resend/",
        ActivationResendApiView.as_view(),
        name="activation-resend",
    ),
    # Reset Password:
    path(
        "reset-password/request/",
        ResetPasswordRequestAPIView.as_view(),
        name="reset-password-request",
    ),
    path(
        "reset-password/confirm/<str:token>/",
        ResetPasswordConfirmAPIView.as_view(),
        name="reset-password-confirm",
    ),
    # Email Send Test:
    # path("test-email/", TestEmailSend.as_view(), name="test-email"),
]
