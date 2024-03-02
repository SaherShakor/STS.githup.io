# Third-part library imports
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from typing import Any

# Local modules imports
from sts.models import *

# Django imports
from django.contrib.auth.password_validation import validate_password




class SignupSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(max_length=64, write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(max_length=64, write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'password2', 'phone_number']
        #? To not show the password
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        #? Hashing the password
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)

        instance.save()
        return instance
    
    def validate(self, attrs):

       password, password2 = attrs.get("password"), attrs.pop("password2")

       if password != password2:
           raise serializers.ValidationError({"password": "Password fields must match."})

       return attrs


class VerifyAccountSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6, min_length=6, required=True)
    
    def validate_otp(self, otp):
        if not otp.isdigit():
            raise serializers.ValidationError("OTP should only contain digits.")
        
        if len(otp) != 6:
            raise serializers.ValidationError("OTP should be a six-digit code.")
        
        return otp

class CaptainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Captain
        fields = '__all__'

        
class LogInSerializer(TokenObtainPairSerializer):
    
    default_error_messages = {
        'detail': 'Invalid email or password.'  # Use your preferred message here
    }

    
    def validate(self, attrs: dict[str, Any]) -> dict[str, str]:
        attrs = super().validate(attrs)
        user = self.user
       
        if not user.is_verified:
            raise serializers.ValidationError({'is_verified':'Your account is not verified, please verify confirm your email'})
    
        return attrs

class OTPcheck(serializers.Serializer):
    otp = serializers.CharField(max_length = 6)


class UserDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'



class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'


class UserOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'name', 'phone_number', 'location')