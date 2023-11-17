
from django.urls import path
from .views import EventAPIView, HostAPIView, EventRsvpAPIView, verify_event, verify_rsvp

urlpatterns = [
    path('event/', EventAPIView.as_view(), name='event'),
    path(
        'event/<str:identifier>/',
        EventAPIView.as_view(),
        name='event_by_identifier'
    ),
    path('host/', HostAPIView.as_view(), name='host'),
    path('host/<int:pk>/', HostAPIView.as_view(), name='host_by_id'),
    path('event-rsvp/', EventRsvpAPIView.as_view(), name='host'),
    path('event-rsvp/<int:pk>/', EventRsvpAPIView.as_view(), name='host_by_id'),
    path('verify-event/<str:token>/', verify_event, name='verify_event'),
    path('verify-rsvp/<str:token>/', verify_rsvp, name='verify_rsvp'),
]
