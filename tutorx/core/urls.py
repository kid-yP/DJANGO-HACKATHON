# urls.py
from django.urls import path
from .views import (
    ClientDashboardAPIView,
    TutorBookingCreateView,
    TutorNotificationListView,
    TutorRequestCreateView,
    TutorProfileUpdateView,
    TutorDashboardAPIView,
    TutorNotificationDetailView,
    ClientNotificationListView
)

urlpatterns = [
    path('api/client/dashboard', ClientDashboardAPIView.as_view(), name='tutor-list'),
    path('api/client/dashboard/<int:client_id>/client-notifications/', ClientNotificationListView.as_view(), name='tutor-list'),
    path('api/tutor/dashboard/', TutorDashboardAPIView.as_view(), name='tutor-dashboard'),
    path('api/tutor-profile/update/<int:pk>/', TutorProfileUpdateView.as_view(), name='tutor_profile_update'),
    path('api/tutor/<int:tutor_id>/booking/', TutorBookingCreateView.as_view(), name='book-tutor'),
    path('api/tutor/dashboard/<int:tutor_id>/tutor-notifications/', TutorNotificationListView.as_view(), name='notification-list'),
    path('api/tutor/dashboard/<int:tutor_id>/tutor-notifications/<int:pk>/', TutorNotificationDetailView.as_view(), name='notification-detail'),
    path('api/send-tutor-request/', TutorRequestCreateView.as_view(), name='send-tutor-request'),
]
