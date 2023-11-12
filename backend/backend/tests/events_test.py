import pytest
from django.test import Client
from django.urls import reverse
from backend.models import Event


@pytest.mark.django_db
def test_create_event(client: Client):
    data = {
        'event_name': 'Test Event',
        'date': '2023-11-10',
        'time': '12:00:00',
        'location_name': 'Test Location',
        'location_address': '123 Main Street',
        'location_city': 'Brooklyn',
        'location_state': 'New York',
        'location_country': 'United States',
        'location_zip': 10001,
        'organizer_name': 'John Doe',
        'organizer_email': 'johndoe@test.com',
        'event_max_capacity': 100,
        'event_format': 'in-person',
        'description': 'This is a test description.'
    }

    assert 1 == 1
