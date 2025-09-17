from rest_framework import generics,status
from .serializers import RegistrationSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

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

