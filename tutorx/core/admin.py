from django.contrib import admin
from .models import *
from user.models import CustomUser,Tutor,Client

@admin.register(TutorBooking)
class TutorBookingAdmin(admin.ModelAdmin):
    list_display = ['client_full_name', 'tutor_full_name', 'is_virtual', 'is_in_person', 'created_at']
    def client_full_name(self, obj):
        return obj.client.user.full_name  if obj.client else ''

    def tutor_full_name(self, obj):
        return obj.tutor.user.full_name if obj.tutor else ''

@admin.register(TutorNotification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('client_username', 'message', 'created_at','is_approved','is_declined')

    def client_username(self, obj):
        return obj.client.user.username
    
    client_username.short_description = 'Client Username'
@admin.register(ClientNotification)
class NotificationCAdmin(admin.ModelAdmin):
    list_display = ('tutor_username', 'message', 'created_at')

    def tutor_username(self, obj):
        return obj.tutor.user.username
    
    tutor_username.short_description = 'Tutor Username'

@admin.register(TutorRequest)
class TutorRequestAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('sender__username', 'receiver__username')

