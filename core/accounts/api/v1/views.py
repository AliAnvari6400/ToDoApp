from rest_framework import generics,status
from .serializers import RegistrationSerializer
from rest_framework.response import Response

#registration:
class RegistrationApiView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer
    
    def post(self,request,*args,**kwargs):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {'email':serializer.validated_data['email']}
        return Response(data, status=status.HTTP_201_CREATED)
