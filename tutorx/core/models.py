from django.db import models
from user.models import *

class TutorBooking(models.Model):
    client = models.ForeignKey(Client, related_name='bookings', on_delete=models.CASCADE)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    is_virtual = models.BooleanField(default=False)
    is_in_person = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

class TutorNotification(models.Model):
    tutor = models.ForeignKey(Tutor, related_name='notifications_received', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, related_name='notifications_sent', on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    is_declined = models.BooleanField(default=False)
    def approve(self):
        self.is_approved = True
        self.save(update_fields=['is_approved'])

    def decline(self):
        self.is_declined = True
        self.save(update_fields=['is_declined'])
        
class ClientNotification(models.Model):
    tutor = models.ForeignKey(Tutor, related_name='notifications_sent', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, related_name='notifications_received', on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class TutorRequest(models.Model):
    sender = models.ForeignKey(Tutor, related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(Client, related_name='received_requests', on_delete=models.CASCADE)
    message = models.TextField()
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
