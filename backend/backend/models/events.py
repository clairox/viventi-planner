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
