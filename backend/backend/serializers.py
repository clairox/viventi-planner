from rest_framework import serializers
from .models import Event, Host, EventRsvp
from datetime import datetime
from django.utils import timezone


class EventSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        # Remove location fields if event_format === virtual
        data = kwargs.pop('data', None)
        if data is not None and data['event_format'] == 'virtual':
            exclude = ['location_name', 'location_address', 'location_city',
                       'location_state', 'location_country', 'location_zip']
            for key in exclude:
                data.pop(key, None)

        kwargs = {"data": data}
        super(EventSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Event
        exclude = ['event_slug', 'edit_token']
        read_only_fields = ['verified', 'created_at', 'modified_at']

    def create(self, validated_data):
        date = validated_data.get('date')
        time = validated_data.get('time')

        validated_data['event_datetime'] = timezone.make_aware(
            datetime.combine(date, time)
        )
        validated_data['status'] = 'inactive'

        return Event.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.modified_at = timezone.now()
        return super().update(instance, validated_data)


class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Host
        fields = '__all__'
        read_only_fields = ['created_at', 'modified_at']

    def update(self, instance, validated_data):
        instance.host_name = validated_data.get(
            'host_name',
            instance.host_name
        )

        instance.modified_at = timezone.now()

        instance.save()
        return instance


# Only used when not editing
class EventRsvpSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRsvp
        exclude = ['edit_token']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('attendee_email')
        return representation


# Used when editing as RSVP attendee
class EventRsvpWithAttendeeAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRsvp
        exclude = ['edit_token']
        read_only_fields = ['verified', 'blocked', 'created_at', 'modified_at']

    def update(self, instance, validated_data):
        instance.attendee_name = validated_data.get(
            'attendee_name',
            instance.attendee_name
        )
        instance.attendee_email = validated_data.get(
            'attendee_email',
            instance.attendee_email
        )
        instance.rsvp_status = validated_data.get(
            'rsvp_status',
            instance.rsvp_status
        )

        instance.modified_at = timezone.now()

        instance.save()
        return instance


# Used when editing as event organizer
class EventRsvpWithOrganizerAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRsvp
        exclude = ['edit_token']
        read_only_fields = [
            'attendee_name',
            'attendee_email',
            'rsvp_status',
            'verified',
            'created_at',
            'modified_at'
        ]

    def update(self, instance, validated_data):
        instance.blocked = validated_data.get(
            'blocked',
            instance.blocked
        )

        instance.modified_at = timezone.now()

        instance.save()
        return instance
