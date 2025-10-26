from rest_framework import generics, status
from .serializers import (
    RegistrationSerializer,
    ProfileSerializer,
    CustomObtainAuthTokenSerializer,
    ActivationResendSerializer,
    ResetPasswordRequestSerializer,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (
    CustomTokenObtainPairSerializer,
    ChangePasswordSerializer,
    ResetPasswordConfirmSerializer,
)
from rest_framework.generics import GenericAPIView
from ...models import Profile, User
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from rest_framework_simplejwt.tokens import RefreshToken
from ..utils import EmailThread
import jwt
from django.conf import settings
from .permissions import NoPostForLoggedInUsers


# Registration:
class RegistrationApiView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        print(serializer)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()  # get user obj from serializer

        # added token for user in email:
        token = self.get_token_for_user(user)

        # Prepare email content
        subject = "Welcome!"
        from_email = "no-reply@example.com"
        to_email = user.email
        html_content = render_to_string(
            "email/activation_email.html", {"token": token, "user": user}
        )
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        email.attach_alternative(html_content, "text/html")
        # email.send()

        EmailThread(email).start()  # send email via Thread class

        data = {
            "email": serializer.validated_data["email"],
            "detail": "verification email sent",
        }
        return Response(data, status=status.HTTP_201_CREATED)

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


# login by token:
class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = CustomObtainAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {
                "token": token.key,
                "user_id": user.pk,
                "email": user.email,
                "is_verified": user.is_verified,
            }
        )


# logout by token:
class CustomDiscardAuthtoken(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Custom jwt token response:
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# change password:
class ChangepasswordAPIView(GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user

        # Check current password
        if not user.check_password(serializer.validated_data["current_password"]):
            return Response(
                {"current_password": ["Wrong password."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Set new password
        user.set_password(serializer.validated_data["new_password"])
        user.save()

        return Response(
            {"detail": "Password updated successfully."},
            status=status.HTTP_200_OK,
        )


# profile:

# class ProfileAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = ProfileSerializer

#     def get(self, request):
#         profile = Profile.objects.filter(user=request.user)
#         serializer = ProfileSerializer(profile,many=True)
#         return Response(serializer.data)

#     def put(self, request):
#         profile = Profile.objects.get(user=request.user)
#         serializer = ProfileSerializer(profile,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def patch(self, request):
#         profile = Profile.objects.get(user=request.user)
#         serializer = ProfileSerializer(profile,data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    queryset = Profile.objects.all()

    def get_object(self):
        # Return the profile for the logged-in user
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj


# email send test:
# class TestEmailSend(GenericAPIView):
#     def get(self, request, *args, **kwargs):
#         user = request.user  # assuming user is authenticated
#         # added token for user in email:
#         token = self.get_token_for_user(user)

#         # Prepare email content
#         subject = "Welcome!"
#         from_email = "no-reply@example.com"
#         to_email = user.email
#         html_content = render_to_string(
#             "email/activation_email.html", {"token": token, "user": user}
#         )
#         text_content = strip_tags(html_content)
#         email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
#         email.attach_alternative(html_content, "text/html")
#         # email.send()

#         EmailThread(email).start()  # send email via Thread class

#         return Response({"detail": "Welcome email sent."}, status=status.HTTP_200_OK)

#     def get_token_for_user(self, user):
#         refresh = RefreshToken.for_user(user)
#         return str(refresh.access_token)


# Activation:
class ActivationApiView(APIView):
    def get(self, request, token):
        try:
            token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return Response({"error": "Token has expired"}, status=401)
        except jwt.InvalidTokenError:
            return Response({"error": "Invalid token"}, status=401)

        user_id = token.get("user_id")
        user_obj = User.objects.get(pk=user_id)
        if user_obj.is_verified:
            return Response(
                {"details": "user was verified"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user_obj.is_verified = True
        user_obj.save()
        return Response(
            {"details": "your account verified"},
            status=status.HTTP_202_ACCEPTED,
        )


class ActivationResendApiView(GenericAPIView):
    serializer_class = ActivationResendSerializer

    def post(self, request, *args, **kwargs):
        serializer = ActivationResendSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        # added token for user in email:
        token = self.get_token_for_user(user)

        # Prepare email content
        subject = "Welcome!"
        from_email = "no-reply@example.com"
        to_email = user.email
        html_content = render_to_string(
            "email/activation_email.html", {"token": token, "user": user}
        )
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        email.attach_alternative(html_content, "text/html")
        # email.send()

        EmailThread(email).start()  # send email via Thread class
        data = {
            "email": serializer.validated_data["email"],
            "detail": "verification email sent",
        }
        return Response(data, status=status.HTTP_201_CREATED)

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


# Reset Password (request & confirm):
class ResetPasswordRequestAPIView(GenericAPIView):
    serializer_class = ResetPasswordRequestSerializer
    permission_classes = [NoPostForLoggedInUsers]

    def post(self, request, *args, **kwargs):
        # if request.user.is_authenticated:
        #     return Response({"detail": "Logged-in users cannot send POST requests."},
        #                     status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"detail": "If the email exists, a reset link has been sent."},
                status=status.HTTP_200_OK,
            )

        # Generate token
        token = self.get_token_for_user(user)

        # reset url
        reset_url = (
            f"http://127.0.0.1:8000/accounts/api/v1/reset-password/confirm/{token}/"
        )

        # Prepare email content
        subject = "Welcome!"
        from_email = "no-reply@example.com"
        to_email = user.email
        html_content = render_to_string(
            "email/reset_email.html", {"reset_url": reset_url, "user": user}
        )
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        email.attach_alternative(html_content, "text/html")
        # email.send()

        EmailThread(email).start()  # send email via Thread class

        data = {
            "email": serializer.validated_data["email"],
            "detail": "reset link sent",
        }
        return Response(data, status=status.HTTP_200_OK)

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class ResetPasswordConfirmAPIView(GenericAPIView):
    serializer_class = ResetPasswordConfirmSerializer

    def post(self, request, token):
        # Pass token via context to serializer
        serializer = self.get_serializer(
            data=request.data, context={"kwargs": {"token": token}}
        )

        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        new_password = serializer.validated_data["new_password"]

        user.set_password(new_password)
        user.save()
        print(new_password)

        return Response(
            {"detail": "Password reset successful."},
            status=status.HTTP_200_OK,
        )
