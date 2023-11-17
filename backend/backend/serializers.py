from rest_framework import serializers
from .models import Event
from datetime import datetime
from django.utils import timezone


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        exclude = ['event_slug', 'edit_token']
        read_only_fields = ['verified']

    def create(self, validated_data):
        date = validated_data.get('date')
        time = validated_data.get('time')

        validated_data['event_datetime'] = timezone.make_aware(
            datetime.combine(date, time)
        )
        validated_data['status'] = 'inactive'

        return Event.objects.create(**validated_data)
