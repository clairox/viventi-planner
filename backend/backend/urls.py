
from django.urls import path
from .views import EventAPIView, HostAPIView, verify_event

urlpatterns = [
    path('event/', EventAPIView.as_view(), name='event'),
    path(
        'event/<str:identifier>/',
        EventAPIView.as_view(),
        name='event_by_identifier'
    ),
    path('host/', HostAPIView.as_view(), name='host'),
    path('host/<int:pk>/', HostAPIView.as_view(), name='host_by_id'),
    path('verify-event/<str:token>/', verify_event, name='verify_token'),
]
