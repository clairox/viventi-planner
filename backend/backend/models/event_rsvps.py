from .events import Event
from django.db import models
from django.utils import timezone


class EventRsvp(models.Model):
    rsvp_id = models.BigAutoField(primary_key=True)
    # References the event that RSVP is associated with
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    # Token providing admin privileges for updating RSVP
    edit_token = models.CharField(max_length=128, unique=True, null=True)
    attendee_name = models.CharField(max_length=100)
    attendee_email = models.EmailField()
    # True = going, False = not going
    rsvp_status = models.BooleanField(default=True)
    # Indicates if the attendee is blocked from the event
    blocked = models.BooleanField(default=False)
    # Indicates if the RSVP is verified
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'event_rsvp'
        db_table_comment = 'Info about event RSVPs'

        constraints = [
            # Ensure 'attendee_email' is unique per the event it's associated with
            models.UniqueConstraint(
                fields=['event_id', 'attendee_email'],
                name='unique_event_rsvp'
            ),
            # Ensure 'edit_token' contains a value when and only when event is verified
            models.CheckConstraint(
                check=(
                    models.Q(verified=True, edit_token__isnull=False) |
                    models.Q(verified=False, edit_token__isnull=True)
                ),
                name='chk_event_rsvp_verified_fields'
            )
        ]
