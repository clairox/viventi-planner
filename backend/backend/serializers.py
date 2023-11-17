from rest_framework import serializers
from .models import Event, Host, EventRsvp
from datetime import datetime
from django.utils import timezone


# TODO updated modified_at on every update
class EventSerializer(serializers.ModelSerializer):
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

        instance.save()
        return instance


class EventRsvpSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRsvp
        exclude = ['attendee_email']
        read_only_fields = ['created_at', 'modified_at']
