# models.py
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

class CustomUser(AbstractUser):
    STUDENT_ROLE = 'S'
    PARENT_ROLE = 'P'
    TUTOR_ROLE = 'T'
    ROLE_CHOICES = [
        (STUDENT_ROLE, 'Student'),
        (PARENT_ROLE, 'Parent'),
        (TUTOR_ROLE, 'Tutor')
    ]
   
    full_name = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=150, unique=True)
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=100, blank=True, null=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []  

    def __str__(self):
        return self.first_name

class Client(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='client')
    role = models.CharField(max_length=10, choices=CustomUser.ROLE_CHOICES)
    #username = models.CharField(max_length=150, unique=True)
    #email = models.EmailField(unique=True)
    #password = models.CharField(max_length=128)
    #full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    subject = models.CharField(max_length=100)
    level = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.user.first_name


class Tutor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='tutor')
    #username = models.CharField(max_length=150, unique=True)
    #email = models.EmailField(unique=True)
    #full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    level = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    bio = models.TextField()
    profile = models.ImageField(upload_to='tutor_profiles/', null=True, blank=True)
    working_days = models.CharField(max_length=255)
    uni = models.CharField(max_length=255)
    education = models.TextField()
    cv = models.FileField(upload_to='cv/') 
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.user.role = CustomUser.TUTOR_ROLE
            self.user.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.first_name