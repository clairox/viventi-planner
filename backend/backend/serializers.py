from rest_framework import serializers
from .models import Event
from datetime import datetime
from django.utils import timezone


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

    def to_internal_value(self, data):
        date_str = data.get('date')
        time_str = data.get('time')

        if date_str is not None and time_str is not None:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            time = datetime.strptime(time_str, "%H:%M:%S").time()
            data['event_datetime'] = timezone.make_aware(
                datetime.combine(date, time)
            )

        return super().to_internal_value(data)

    def create(self, validated_data):
        validated_data['status'] = 'inactive'
        validated_data['verified'] = False

        return Event.objects.create(**validated_data)

    # TODO can't update any values besides status
    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
