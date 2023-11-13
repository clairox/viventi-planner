# Generated by Django 4.2.7 on 2023-11-13 14:17

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('event_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('event_slug', models.CharField(max_length=64, null=True, unique=True)),
                ('event_name', models.CharField(max_length=50)),
                ('edit_token', models.CharField(max_length=128, null=True, unique=True)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('event_datetime', models.DateTimeField()),
                ('location_name', models.CharField(blank=True, max_length=100, null=True)),
                ('location_address', models.CharField(blank=True, max_length=255, null=True)),
                ('location_city', models.CharField(blank=True, max_length=100, null=True)),
                ('location_state', models.CharField(blank=True, max_length=100, null=True)),
                ('location_country', models.CharField(blank=True, max_length=100, null=True)),
                ('location_zip', models.CharField(blank=True, max_length=20, null=True)),
                ('organizer_name', models.CharField(max_length=100)),
                ('organizer_email', models.EmailField(max_length=254)),
                ('event_max_capacity', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('event_format', models.CharField(choices=[('virtual', 'Virtual'), ('in-person', 'In person')], max_length=20)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('inactive', 'Inactive'), ('verified', 'Verified'), ('canceled', 'Canceled'), ('completed', 'Completed')], default='inactive', max_length=20)),
                ('verified', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'event',
                'db_table_comment': 'Info about events',
            },
        ),
        migrations.CreateModel(
            name='EventRsvp',
            fields=[
                ('rsvp_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('edit_token', models.CharField(max_length=128, null=True, unique=True)),
                ('attendee_name', models.CharField(max_length=100)),
                ('attendee_email', models.EmailField(max_length=254)),
                ('rsvp_status', models.BooleanField(default=True)),
                ('blocked', models.BooleanField(default=False)),
                ('verified', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'event_rsvp',
                'db_table_comment': 'Info about event RSVPs',
            },
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('host_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('host_name', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'host',
                'db_table_comment': 'Info about event hosts',
            },
        ),
        migrations.CreateModel(
            name='VerificationToken',
            fields=[
                ('token_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('token_value', models.CharField(max_length=128)),
                ('token_type', models.CharField(choices=[{'Event', 'event'}, ('rsvp', 'RSVP')], max_length=20)),
                ('associated_event_id', models.BigIntegerField(null=True)),
                ('associated_rsvp_id', models.BigIntegerField(null=True)),
                ('expiry_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'verification_token',
                'db_table_comment': 'Verification tokens for events and RSVPs',
            },
        ),
        migrations.AddConstraint(
            model_name='verificationtoken',
            constraint=models.CheckConstraint(check=models.Q(('token_type__in', ['event', 'rsvp'])), name='check_token_type'),
        ),
        migrations.AddConstraint(
            model_name='verificationtoken',
            constraint=models.CheckConstraint(check=models.Q(('expiry_datetime__gte', datetime.datetime(2023, 11, 13, 14, 17, 47, 280580, tzinfo=datetime.timezone.utc))), name='expiry_datetime_not_in_past'),
        ),
        migrations.AddField(
            model_name='host',
            name='event_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.event'),
        ),
        migrations.AddField(
            model_name='eventrsvp',
            name='event_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.event'),
        ),
        migrations.AddConstraint(
            model_name='event',
            constraint=models.CheckConstraint(check=models.Q(('event_max_capacity__gte', 0)), name='chk_capacity_not_negative'),
        ),
        migrations.AddConstraint(
            model_name='event',
            constraint=models.CheckConstraint(check=models.Q(('status__in', ['inactive', 'verified', 'canceled', 'completed'])), name='check_status'),
        ),
        migrations.AddConstraint(
            model_name='event',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('edit_token__isnull', False), ('event_slug__isnull', False), ('verified', True)), models.Q(('edit_token__isnull', True), ('event_slug__isnull', True), ('verified', False)), _connector='OR'), name='chk_event_verified_fields'),
        ),
        migrations.AddConstraint(
            model_name='event',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('event_format__exact', 'in-person'), ('location_address__isnull', False), ('location_city__isnull', False), ('location_country__isnull', False), ('location_state__isnull', False), ('location_zip__isnull', False)), models.Q(('event_format__exact', 'virtual'), ('location_address__isnull', True), ('location_city__isnull', True), ('location_country__isnull', True), ('location_name__isnull', True), ('location_state__isnull', True), ('location_zip__isnull', True)), _connector='OR'), name='chk_virtual_location'),
        ),
        migrations.AddConstraint(
            model_name='eventrsvp',
            constraint=models.UniqueConstraint(fields=('event_id', 'attendee_email'), name='unique_event_rsvp'),
        ),
        migrations.AddConstraint(
            model_name='eventrsvp',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('edit_token__isnull', False), ('verified', True)), models.Q(('edit_token__isnull', True), ('verified', False)), _connector='OR'), name='chk_event_rsvp_verified_fields'),
        ),
    ]
