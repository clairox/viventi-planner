from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone


class Event(models.Model):
    event_id = models.BigAutoField(primary_key=True)
    event_slug = models.CharField(max_length=64, unique=True, null=True)
    event_name = models.CharField(max_length=50)
    # Token providing admin privileges for editing event
    edit_token = models.CharField(max_length=128, unique=True, null=True)
    date = models.DateField()  # Date of the event
    time = models.TimeField()  # Time of the event
    event_datetime = models.DateTimeField()
    location_name = models.CharField(max_length=100, null=True, blank=True)
    location_address = models.CharField(max_length=255, null=True, blank=True)
    location_city = models.CharField(max_length=100, null=True, blank=True)
    location_state = models.CharField(max_length=100, null=True, blank=True)
    location_country = models.CharField(max_length=100, null=True, blank=True)
    location_zip = models.CharField(max_length=20, null=True, blank=True)
    organizer_name = models.CharField(max_length=100)
    organizer_email = models.EmailField()
    event_max_capacity = models.IntegerField(validators=[MinValueValidator(0)])
    EVENT_FORMAT_CHOICES = [('virtual', 'Virtual'), ('in-person', 'In person')]
    event_format = models.CharField(
        max_length=20, choices=EVENT_FORMAT_CHOICES)
    description = models.TextField()  # Description for the event
    STATUS_CHOICES = [('inactive', 'Inactive'), ('verified', 'Verified'),
                      ('canceled', 'Canceled'), ('completed', 'Completed')]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    # Indicates if the event is verified
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'event'
        db_table_comment = 'Info about events'

        constraints = [
            # Ensure 'event_max_capacity' is not negative
            models.CheckConstraint(
                check=models.Q(event_max_capacity__gte=0),
                name='chk_capacity_not_negative'
            ),
            # Ensure 'status' is one of the predefined choices
            models.CheckConstraint(
                check=models.Q(
                    status__in=['inactive', 'verified', 'canceled', 'completed']),
                name='check_status'
            ),
            # Ensure 'event_slug' and 'edit_token' contain values when and only when event is verified
            models.CheckConstraint(
                check=(
                    models.Q(
                        verified=True,
                        event_slug__isnull=False,
                        edit_token__isnull=False
                    ) |
                    models.Q(
                        verified=False,
                        event_slug__isnull=True,
                        edit_token__isnull=True
                    )
                ),
                name='chk_event_verified_fields'
            ),
            # Ensures virtual events have specific location fields set to NULL
            models.CheckConstraint(
                check=(
                    models.Q(
                        event_format__exact='in-person',
                        location_address__isnull=False,
                        location_city__isnull=False,
                        location_state__isnull=False,
                        location_country__isnull=False,
                        location_zip__isnull=False
                    ) |
                    models.Q(
                        event_format__exact='virtual',
                        location_name__isnull=True,
                        location_address__isnull=True,
                        location_city__isnull=True,
                        location_state__isnull=True,
                        location_country__isnull=True,
                        location_zip__isnull=True
                    )
                ),
                name='chk_virtual_location'
            )
        ]


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
