from django.db import models
from django.utils import timezone


class VerificationToken(models.Model):
    token_id = models.BigAutoField(primary_key=True)
    token_value = models.CharField(max_length=128)
    TOKEN_TYPE_CHOICES = [{'event', 'Event'}, ('rsvp', 'RSVP')]
    token_type = models.CharField(max_length=20, choices=TOKEN_TYPE_CHOICES)
    associated_event_id = models.BigIntegerField(null=True)
    associated_rsvp_id = models.BigIntegerField(null=True)
    expiry_datetime = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'verification_token'
        db_table_comment = 'Verification tokens for events and RSVPs'

        constraints = [
            # Ensure 'token_type' is one of the predefined choices
            models.CheckConstraint(
                check=models.Q(token_type__in=['event', 'rsvp']),
                name='check_token_type'
            ),
            # Ensure 'expiry_datetime' is not in the past
            models.CheckConstraint(
                check=models.Q(expiry_datetime__gte=timezone.now()),
                name='expiry_datetime_not_in_past'
            )
        ]
