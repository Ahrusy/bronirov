from django.core.management.base import BaseCommand
from events.models import Event
from datetime import date

class Command(BaseCommand):
    help = 'Add a test event to Event model'

    def handle(self, *args, **kwargs):
        Event.objects.create(
            title="Sample Concert",
            description="A great concert",
            event_date=date(2025, 6, 1),
            ticket_price=50.00,
            available_tickets=100
        )
        self.stdout.write(self.style.SUCCESS('Test event added')) 