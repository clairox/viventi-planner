import pytest
from django.test import Client
from django.urls import reverse
from backend.models import Event


@pytest.mark.django_db
def test_create_in_person_event_with_valid_data(client: Client):
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

    response = client.post(reverse("event"), data)
    assert response.status_code == 201

    created_event = Event.objects.latest('event_id')
    assert created_event.event_name == 'Test Event'


@pytest.mark.django_db
def test_create_virtual_event_with_valid_data(client: Client):
    data = {
        'event_name': 'Test Event',
        'date': '2023-11-10',
        'time': '12:00:00',
        'organizer_name': 'John Doe',
        'organizer_email': 'johndoe@test.com',
        'event_max_capacity': 100,
        'event_format': 'virtual',
        'description': 'This is a test description.'
    }

    response = client.post(reverse("event"), data)

    assert response.status_code == 201

    created_event = Event.objects.latest('event_id')
    assert created_event.event_name == 'Test Event'


@pytest.mark.django_db
def test_create_event_with_invalid_data(client: Client):
    data = {
        'event_name': '',
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

    response = client.post(reverse("event"), data)

    assert response.status_code == 400
    assert 'event_name' in response.json().get('error')


@pytest.mark.django_db
def test_create_event_with_verified_fields(client: Client):
    data = {
        'event_name': 'Test Event',
        'date': '2023-11-10',
        'time': '12:00:00',
        'organizer_name': 'John Doe',
        'organizer_email': 'johndoe@test.com',
        'event_max_capacity': 100,
        'event_format': 'virtual',
        'description': 'This is a test description.',
        'event_slug': 'test-event-slug',
        'edit_token': 'test-edit-token'
    }

    response = client.post(reverse("event"), data)
    assert response.status_code == 400
    assert response.json().get('error') == 'IntegrityError'


@pytest.mark.django_db
# Should violate 'chk_virtual_location' constraint
def test_create_in_person_event_without_location_data(client: Client):
    data = {
        'event_name': 'Test Event',
        'date': '2023-11-10',
        'time': '12:00:00',
        'organizer_name': 'John Doe',
        'organizer_email': 'johndoe@test.com',
        'event_max_capacity': 100,
        'event_format': 'in-person',
        'description': 'This is a test description.'
    }

    response = client.post(reverse("event"), data)

    assert response.status_code == 400
    assert response.json().get('error') == 'IntegrityError'


@pytest.mark.django_db
# Should violate 'chk_virtual_location' constraint
def test_create_virtual_event_with_location_data(client: Client):
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
        'event_format': 'virtual',
        'description': 'This is a test description.'
    }

    response = client.post(reverse("event"), data)

    assert response.status_code == 400
    assert response.json().get('error') == 'IntegrityError'
