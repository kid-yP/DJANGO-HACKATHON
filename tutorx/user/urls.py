from django.urls import path
from .views import (
    ClientRegistrationAPIView,

    TutorRegistrationAPIView,
    VerifyEmailAPIView,
    UserLoginAPIView,
)

urlpatterns = [
    path('api/client-registration/', ClientRegistrationAPIView.as_view(), name='parent_registration_api'),
    path('api/tutor-registration/', TutorRegistrationAPIView.as_view(), name='tutor_registration_api'),
    path('api/verify-email/<str:uidb64>/<str:token>/', VerifyEmailAPIView.as_view(), name='verify_email_api'),
    path('api/login/', UserLoginAPIView.as_view(), name='user_login_api'),
]


