from rest_framework import generics,status
from .serializers import RegistrationSerializer,ProfileSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer,ChangePasswordSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from ...models import Profile
from django.shortcuts import get_object_or_404

#registration:
class RegistrationApiView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer
    
    def post(self,request,*args,**kwargs):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {'email':serializer.validated_data['email']}
        return Response(data, status=status.HTTP_201_CREATED)

# logout by token:
class CustomDiscardAuthtoken(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
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
        if not user.check_password(serializer.validated_data['current_password']):
            return Response({'current_password': ['Wrong password.']}, status=status.HTTP_400_BAD_REQUEST)

        # Set new password
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response({'detail': 'Password updated successfully.'}, status=status.HTTP_200_OK)

# profile (get/put/patch):
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
        obj = get_object_or_404(queryset,user=self.request.user)
        return obj