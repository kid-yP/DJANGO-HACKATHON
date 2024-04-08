# views.py
from django.shortcuts import get_object_or_404
from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import *
from .serializers import *

class ClientDashboardAPIView(generics.ListAPIView):
    serializer_class = TutorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Tutor.objects.all()
    
class TutorDashboardAPIView(generics.ListAPIView):
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Client.objects.all() 
    
class TutorProfileUpdateView(generics.UpdateAPIView):
    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer
    permission_classes = [IsAuthenticated]

class TutorBookingCreateView(generics.CreateAPIView):
    queryset = TutorBooking.objects.all()
    serializer_class = TutorBookingSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['tutor_id'] = self.kwargs.get('tutor_id')
        return context
    
    def perform_create(self, serializer):
        tutor_id = self.kwargs.get('tutor_id')
        serializer.save()

        tutor = get_object_or_404(Tutor, id=tutor_id)
        client = self.request.user.client
        
        message = f"A new booking request has been made by {client.user.full_name}."
        TutorNotification.objects.create(tutor=tutor, client=client, message=message)


class TutorNotificationListView(generics.ListAPIView):
    serializer_class = TutorNotificationSerializer

    def get_queryset(self):
        tutor_id = self.kwargs.get('tutor_id')
        return TutorNotification.objects.filter(tutor_id=tutor_id)
    
class ClientNotificationListView(generics.ListAPIView):
    serializer_class = ClientNotificationSerializer

    def get_queryset(self):
        client_id = self.kwargs.get('client_id')
        return ClientNotification.objects.filter(client_id=client_id)

class TutorNotificationDetailView(generics.UpdateAPIView):
    queryset = TutorNotification.objects.all()
    serializer_class = TutorNotificationDSerializer
    lookup_url_kwarg = 'pk'
    
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        is_approved = request.data.get('is_approved')
        is_declined = request.data.get('is_declined')
        """print(request.data)
        print("Is Approved:", is_approved)
        print("Is Declined:", is_declined)
"""
        if is_approved == 'true':
            instance.is_approved = True
            instance.is_declined = False 
            instance.save()

            ClientNotification.objects.create(client_id=instance.client_id, tutor_id=instance.tutor_id, message=f"{instance.tutor.user.full_name}'s has approved your request.")
            instance.delete() 
            return Response({'message': 'You have approved the request'}, status=status.HTTP_200_OK)
        
        elif is_declined == 'true':
            instance.is_declined = True
            instance.is_approved = False 
            instance.save()
        
            ClientNotification.objects.create(client_id=instance.client_id, tutor_id=instance.tutor_id, message=f"{instance.tutor.user.full_name}'s has declined your request.")
            instance.delete() 
            return Response({'message': 'You have declined the request'}, status=status.HTTP_200_OK)
        
        else:
            return Response({'error': 'Invalid value for approval or decline status'}, status=status.HTTP_400_BAD_REQUEST)

class TutorRequestCreateView(generics.CreateAPIView):
    serializer_class = TutorRequestSerializer

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
