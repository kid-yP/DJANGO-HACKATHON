from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView,CreateAPIView
from rest_framework.permissions import AllowAny
#from .forms import ParentRegistrationForm, StudentRegistrationForm, TutorRegistrationForm, UserLoginForm
from .models import CustomUser,Tutor,Client
from django.contrib.auth import authenticate, login
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from rest_framework import generics
from django.db import IntegrityError,transaction
    
from .serializers import (
    ClientRegistrationSerializer,
    TutorRegistrationSerializer,
    VerifyEmailSerializer,
    UserLoginSerializer,
    TutorSerializer
)

class TutorListView(generics.ListAPIView):
    queryset = CustomUser.objects.filter(role='T')
    serializer_class = TutorSerializer

class ClientRegistrationAPIView(ListAPIView):
    queryset = CustomUser.objects.none()  
    serializer_class = ClientRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.validated_data
            try:
                user = CustomUser.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    password=user_data['password'],
                    role = user_data.get('role'),
                    is_active=False,
                    full_name=user_data['full_name'],
                )
                client = Client.objects.create(
                    user=user,
                    phone_number=user_data['phone_number'],
                    subject=user_data['subject'],
                    level=user_data['level'],
                    location=user_data['location']
                )
                self.send_verification_email(request, user)
                return Response({'detail': 'Registration successful. Please check your email to verify your account.'}, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                if 'UNIQUE constraint failed: user_customuser.username' in str(e):
                    return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)
                elif 'UNIQUE constraint failed: user_customuser.email' in str(e):
                    return Response({'error': 'Email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def send_verification_email(self, request, user):
        current_site = get_current_site(request)
        mail_subject = 'Activate your account'
        message = render_to_string('verification_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        to_email = user.email
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
    

class TutorRegistrationAPIView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = TutorRegistrationSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    tutor = serializer.save()
                    tutor.user.role = 'T'
                    tutor.user.is_active = False
                    tutor.user.save()
                self.send_verification_email(request, tutor.user)
                return Response({'detail': 'Registration successful. Please check your email to verify your account.'}, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_verification_email(self, request, user):
        current_site = get_current_site(request)
        mail_subject = 'Activate your account'
        message = render_to_string('verification_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        to_email = user.email
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()

class VerifyEmailAPIView(APIView):
    def get(self, request, uidb64, token):
        serializer = VerifyEmailSerializer(data={'uidb64': uidb64, 'token': token})
        if serializer.is_valid():
            try:
                uid = urlsafe_base64_decode(serializer.validated_data['uidb64']).decode()
                user = CustomUser.objects.get(pk=uid)
            except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
                user = None
            if user is not None and default_token_generator.check_token(user, serializer.validated_data['token']):
                user.is_active = True
                user.save()
                messages.success(request, 'Your email has been verified. You can now login.')
                return Response({'detail': 'Your email has been verified. You can now login.'}, status=status.HTTP_200_OK)
            else:
                messages.error(request, 'Invalid verification link.')
                return Response({'detail': 'Invalid verification link.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginAPIView(ListAPIView):
    queryset = CustomUser.objects.none()
    serializer_class = UserLoginSerializer
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f"Hello {user.email}! You have been logged in")
                    return Response({'detail': f'Hello {user.email}! You have been logged in'}, status=status.HTTP_200_OK)
                else:
                    messages.error(request, 'Your account is not yet verified. Please check your email to verify your account.')
                    return Response({'detail': 'Your account is not yet verified. Please check your email to verify your account.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                messages.error(request, "Invalid email or password")
                return Response({'detail': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
