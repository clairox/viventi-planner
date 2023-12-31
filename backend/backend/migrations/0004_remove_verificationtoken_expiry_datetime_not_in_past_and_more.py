# Generated by Django 4.2.7 on 2023-12-13 17:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_remove_eventrsvp_unique_event_rsvp_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='verificationtoken',
            name='expiry_datetime_not_in_past',
        ),
        migrations.AddField(
            model_name='event',
            name='tz_name',
            field=models.CharField(default='America/New_York', max_length=256),
            preserve_default=False,
        ),
        migrations.AddConstraint(
            model_name='verificationtoken',
            constraint=models.CheckConstraint(check=models.Q(('expiry_datetime__gte', datetime.datetime(
                2023, 12, 13, 17, 17, 43, 273237, tzinfo=datetime.timezone.utc))), name='expiry_datetime_not_in_past'),
        ),
    ]
