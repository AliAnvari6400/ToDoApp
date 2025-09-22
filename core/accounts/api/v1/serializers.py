from rest_framework import serializers
from ...models import User,Profile
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate

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


# Customize token serializer for checking user is_verified:
class CustomObtainAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(label="email")
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True,
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                raise serializers.ValidationError("Unable to log in with provided credentials.", code='authorization')
            
            # Check if user is verified
            if not getattr(user, 'is_verified', False):
                raise serializers.ValidationError("User is not verified")
            
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'.", code='authorization')

        attrs['user'] = user
        return attrs
    

 # Add more response data in JWT:
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        data = super().validate(attrs)
        if not self.user.is_verified: # check the verification of user
            raise serializers.ValidationError({'details':'user is not verified'})
        data['email'] = self.user.email
        data['user_id'] = self.user.id
        return data   
    
    
# change password serializer:
class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password_confirm = serializers.CharField(required=True)

    def validate(self, data):
        
        user = self.context['request'].user # Check if the user is verified
        if not getattr(user, 'is_verified', False):
            raise serializers.ValidationError("User is not verified.")
        
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError("New passwords do not match.")
    
        # Validate password strength
        validate_password(data['new_password'])
        return data


# profile serializer:
class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    class Meta:
        model = Profile
        fields = ['id','email','first_name','last_name','image','description']
    
    def validate(self, data):  # check the verification of user
        user = self.context['request'].user
        if not getattr(user, 'is_verified', False):
            raise serializers.ValidationError("User is not verified")
        return data

# Activation Resend: 
class ActivationResendSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    
    def validate(self,attrs):
        email = attrs.get('email')
    
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({'details':'user not exist'})
        if user_obj.is_verified:
            raise serializers.ValidationError({'details':'user already verified'})
        attrs['user'] = user_obj
        return super().validate(attrs) 
        