from rest_framework import serializers
from .models import Event
from datetime import datetime
from django.utils import timezone


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

    def create(self, validated_data):
        date = validated_data.get('date')
        time = validated_data.get('time')

        validated_data['event_datetime'] = timezone.make_aware(
            datetime.combine(date, time)
        )
        validated_data['status'] = 'inactive'
        validated_data['verified'] = False

        return Event.objects.create(**validated_data)

    # TODO can't update any values besides status
    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
