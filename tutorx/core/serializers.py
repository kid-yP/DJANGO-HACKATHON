# serializers.py
from rest_framework import serializers
from .models import *

class TutorSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='user.email', read_only=True)
    full_name = serializers.CharField(source='user.full_name', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Tutor
        fields = ['id','email', 'full_name', 'username', 'bio', 'level', 'location','profile']
        
class ClientSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='user.email', read_only=True)
    full_name = serializers.CharField(source='user.full_name', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    role = serializers.CharField(source='user.role', read_only=True) 
    class Meta:
        model = Client
        fields = '__all__'

class TutorBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorBooking
        fields = ['is_virtual', 'is_in_person', 'created_at']

    def create(self, validated_data):
        tutor_id = self.context.get('tutor_id')
        client = self.context['request'].user.client  # Assuming client is logged in
        return TutorBooking.objects.create(tutor_id=tutor_id, client=client, **validated_data)

class TutorNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorNotification
        #fields = ['is_approved','is_declined']
        fields = '__all__'
class TutorNotificationDSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorNotification
        fields = ['is_approved','is_declined']
        #fields = '__all__'
class ClientNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientNotification
        fields = '__all__'

class TutorRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorRequest
        fields = '__all__'
