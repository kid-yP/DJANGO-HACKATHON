from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import *


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'full_name', 'email', 'phone_number', 'role']

class ClientRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    full_name = serializers.CharField()
    
    class Meta:
        model = Client
        fields = ['username', 'email', 'password', 'role', 'full_name', 'phone_number', 'subject', 'level', 'location']
        extra_kwargs = {'password': {'write_only': True}}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].choices = CustomUser.ROLE_CHOICES[:2]
    """def create(self, validated_data):
        user_data = {field: validated_data.pop(field) for field in ['username', 'email', 'password', 'full_name']}
        user = CustomUser.objects.create(**user_data)
        client = Client.objects.create(user=user, **validated_data)
        return client"""


class TutorRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    full_name = serializers.CharField()

    class Meta:
        model = Tutor
        fields = ['username', 'email', 'password', 'full_name', 'phone_number', 'level', 'bio', 'working_days', 'uni', 'education','location', 'cv']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user_data = {field: validated_data.pop(field) for field in ['username', 'email', 'full_name']}
        password = validated_data.pop('password')
        user = CustomUser.objects.create(**user_data, role=CustomUser.TUTOR_ROLE)
        user.set_password(password)
        user.save()
        tutor = Tutor.objects.create(user=user, **validated_data)
        return tutor
    
class VerifyEmailSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'full_name', 'email', 'phone_number', 'role', 'subject', 'level', 'location', 'bio', 'date_of_birth']

class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'full_name', 'email', 'phone_number', 'role', 'location', 'bio']

class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'full_name', 'email', 'phone_number', 'role2', 'subject', 'level', 'location', 'bio', 'uni', 'education', 'working_days', 'description', 'image', 'virtual', 'rating']

