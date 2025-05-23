from django.core.management.base import BaseCommand
from events.models import Event
import requests
import time

class Command(BaseCommand):
    help = 'Обновляет поле event_url у импортированных событий через API KudaGo по external_id'

    def handle(self, *args, **kwargs):
        updated = 0
        for event in Event.objects.filter(is_imported=True, event_url__isnull=True):
            if not event.external_id:
                continue
            url = f'https://kudago.com/public-api/v1.4/events/{event.external_id}/?lang=ru'
            resp = requests.get(url)
            time.sleep(0.2)
            if resp.status_code == 200:
                data = resp.json()
                site_url = data.get('site_url')
                if site_url:
                    event.event_url = site_url
                    event.save()
                    updated += 1
                    self.stdout.write(self.style.SUCCESS(f'{event.title} -> {site_url}'))
        self.stdout.write(self.style.SUCCESS(f'Обновлено событий: {updated}')) 