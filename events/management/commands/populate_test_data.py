from django.core.management.base import BaseCommand
from django.db import transaction
from events.models import City, Location, Genre, Event
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Populate database with test data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating test data...')

        with transaction.atomic():
            # Создаем города
            cities = [
                {'name': 'Москва', 'slug': 'moscow'},
                {'name': 'Санкт-Петербург', 'slug': 'spb'},
                {'name': 'Онлайн', 'slug': 'online'},
            ]
            for city_data in cities:
                city, created = City.objects.get_or_create(
                    slug=city_data['slug'],
                    defaults={'name': city_data['name']}
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created city: {city.name}'))

            # Создаем жанры
            genres = ['Концерт', 'Выставка', 'Театр', 'Кино', 'Фестиваль']
            for genre_name in genres:
                genre, created = Genre.objects.get_or_create(name=genre_name)
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created genre: {genre.name}'))

            # Создаем места проведения
            locations = [
                {'name': 'Крокус Сити Холл', 'city': 'moscow', 'address': 'Москва, 66-й км МКАД'},
                {'name': 'ДК им. Ленсовета', 'city': 'spb', 'address': 'Санкт-Петербург, Каменноостровский пр., 42'},
            ]
            for loc_data in locations:
                city = City.objects.get(slug=loc_data['city'])
                location, created = Location.objects.get_or_create(
                    name=loc_data['name'],
                    city=city,
                    defaults={'address': loc_data['address']}
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created location: {location.name}'))

            # Создаем мероприятия
            events = [
                {
                    'title': 'Рок-фестиваль 2024',
                    'description': 'Грандиозный рок-фестиваль с участием лучших групп',
                    'genre': 'Фестиваль',
                    'city': 'moscow',
                    'location': 'Крокус Сити Холл',
                    'ticket_price': 3000.00,
                },
                {
                    'title': 'Выставка современного искусства',
                    'description': 'Экспозиция работ современных художников',
                    'genre': 'Выставка',
                    'city': 'spb',
                    'location': 'ДК им. Ленсовета',
                    'ticket_price': 500.00,
                },
                {
                    'title': 'Онлайн-концерт',
                    'description': 'Прямая трансляция концерта',
                    'genre': 'Концерт',
                    'city': 'online',
                    'location': None,
                    'ticket_price': 0.00,
                },
            ]

            for event_data in events:
                city = City.objects.get(slug=event_data['city'])
                genre = Genre.objects.get(name=event_data['genre'])
                location = Location.objects.get(name=event_data['location']) if event_data['location'] else None

                event_date = datetime.now().date() + timedelta(days=30)  # Через месяц
                event, created = Event.objects.get_or_create(
                    title=event_data['title'],
                    defaults={
                        'description': event_data['description'],
                        'event_date': event_date,
                        'start_time': datetime.now().time(),
                        'city': city,
                        'location': location,
                        'genre': genre,
                        'ticket_price': event_data['ticket_price'],
                        'available_tickets': 100,
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created event: {event.title}'))

        self.stdout.write(self.style.SUCCESS('Successfully populated test data')) 