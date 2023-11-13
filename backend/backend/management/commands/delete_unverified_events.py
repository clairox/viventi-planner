from django.core.management.base import BaseCommand
from django.utils import timezone
from backend.models import Event


class Command(BaseCommand):
    help = 'Deletes unverified events older than 7 days'

    def handle(self, *args, **options):
        cutoff_time = timezone.now() - timezone.timedelta(days=7)
        events_to_delete = Event.objects.filter(
            status='inactive', created_at__lte=cutoff_time
        )
        delete_count = len(events_to_delete)
        events_to_delete.delete()
        self.stdout.write(self.style.SUCCESS(
            f'Deleted {delete_count} unverified events'
        ))
