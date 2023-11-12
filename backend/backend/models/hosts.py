from .events import Event
from django.db import models
from django.utils import timezone


class Host(models.Model):
    host_id = models.BigAutoField(primary_key=True)
    # Name of the person hosting event
    host_name = models.CharField(max_length=100)
    # References the event that host is associated with
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'host'
        db_table_comment = 'Info about event hosts'
