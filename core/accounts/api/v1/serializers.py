from rest_framework import serializers
from ...models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# registration:
class RegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=255,write_only=True)
    
    class Meta:
        model = User
        fields = ['email','password','password1']
        
    def validate(self,attrs):
        if attrs.get('password')!=attrs.get('password1'):
            raise serializers.ValidationError({'details':'password does not match'})
        try:
            validate_password(attrs.get('password'))
            
        except ValidationError as e:
            raise serializers.ValidationError({'password':list(e.messages)})
        return super().validate(attrs)
    
    def create(self,validated_data):
        validated_data.pop('password1',None)
        return User.objects.create_user(**validated_data)

 # Add more response data in JWT:
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        data = super().validate(attrs)
        data['email'] = self.user.email
        data['user_id'] = self.user.id
        return data   