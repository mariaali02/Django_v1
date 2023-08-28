# apitest/api/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from flipcart.models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =['id','username', 'email', 'password' ]

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user','email', 'date_of_birth', 'gender', 'phone_number']  

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class ResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password','email','date_of_birth', 'gender','phone_number']
        extra_kwargs = {'password': {'write_only': True}}
class SignInSerializer(serializers.Serializer):
    username = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        
        return user