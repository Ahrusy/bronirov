from django.core.management.base import BaseCommand
from events.models import Event
import requests
from bs4 import BeautifulSoup
from datetime import datetime

class Command(BaseCommand):
    help = 'Парсит мероприятия с Афиша.ру (Москва) и добавляет их в базу'

    def handle(self, *args, **kwargs):
        url = 'https://www.afisha.ru/msk/concert/'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        events = soup.select('.c-search-entry')
        count = 0
        for item in events:
            title_tag = item.select_one('.c-search-entry__title')
            date_tag = item.select_one('.c-search-entry__date')
            desc_tag = item.select_one('.c-search-entry__text')
            if not (title_tag and date_tag and desc_tag):
                continue
            title = title_tag.get_text(strip=True)
            date_str = date_tag.get_text(strip=True)
            try:
                event_date = datetime.strptime(date_str, '%d %B %Y').date()
            except Exception:
                event_date = None
            description = desc_tag.get_text(strip=True)
            Event.objects.get_or_create(
                title=title,
                event_date=event_date,
                defaults={
                    'description': description,
                    'ticket_price': 0,
                    'available_tickets': 100,
                }
            )
            count += 1
        self.stdout.write(self.style.SUCCESS(f'Добавлено {count} мероприятий с Афиша.ру')) 