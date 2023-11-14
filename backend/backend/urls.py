
from django.urls import path
from .views import EventAPIView, verify_event

urlpatterns = [
    path('event/', EventAPIView.as_view(), name='event'),
    path(
        'event/<str:identifier>/',
        EventAPIView.as_view(),
        name='event_by_identifier'
    ),
    path('verify-event/<str:token>/', verify_event, name='verify_token'),
]
