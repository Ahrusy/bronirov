from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from events.models import Event, City, Location, Genre
import random

class Command(BaseCommand):
    help = 'Добавляет 3 новых тестовых мероприятия'

    def handle(self, *args, **kwargs):
        self.stdout.write('Добавление тестовых мероприятий...')
        
        # Получаем существующие города, места и жанры или создаем новые
        cities = list(City.objects.all())
        genres = list(Genre.objects.all())
        locations = list(Location.objects.all())
        
        # Если нет данных, создаем базовые
        if not cities:
            cities = [
                City.objects.create(name='Москва', slug='moscow'),
                City.objects.create(name='Санкт-Петербург', slug='spb'),
                City.objects.create(name='Онлайн', slug='online')
            ]
            self.stdout.write(self.style.SUCCESS('Созданы базовые города'))
            
        if not genres:
            genres = [
                Genre.objects.create(name='Концерт'),
                Genre.objects.create(name='Выставка'),
                Genre.objects.create(name='Театр'),
                Genre.objects.create(name='Кино'),
                Genre.objects.create(name='Фестиваль')
            ]
            self.stdout.write(self.style.SUCCESS('Созданы базовые жанры'))
            
        if not locations:
            for city in cities:
                if city.name != 'Онлайн':
                    locations.append(
                        Location.objects.create(
                            name=f'Концертный зал {city.name}', 
                            address=f'ул. Примерная, 1, {city.name}',
                            city=city
                        )
                    )
            self.stdout.write(self.style.SUCCESS('Созданы базовые локации'))
        
        # Создаем данные для новых мероприятий
        events_data = [
            {
                'title': 'Мастер-класс по живописи',
                'description': 'Профессиональный художник научит вас основам живописи маслом за один день!',
                'genre': random.choice(genres),
                'city': cities[0],  # Москва
                'location': next((loc for loc in locations if loc.city == cities[0]), None),
                'ticket_price': 1500.00,
                'event_date': timezone.now().date() + timedelta(days=10),
            },
            {
                'title': 'Джазовый вечер',
                'description': 'Вечер джазовой музыки с лучшими исполнителями города и специальными гостями.',
                'genre': genres[0] if genres else None,  # Концерт
                'city': cities[1],  # Санкт-Петербург
                'location': next((loc for loc in locations if loc.city == cities[1]), None),
                'ticket_price': 2000.00,
                'event_date': timezone.now().date() + timedelta(days=15),
            },
            {
                'title': 'Семинар по программированию',
                'description': 'Онлайн-семинар по современным тенденциям в программировании и разработке.',
                'genre': random.choice(genres),
                'city': cities[2] if len(cities) > 2 else None,  # Онлайн
                'location': None,  # Онлайн мероприятия без локации
                'ticket_price': 500.00,
                'event_date': timezone.now().date() + timedelta(days=5),
            }
        ]
        
        # Создаем мероприятия
        created_count = 0
        for event_data in events_data:
            event = Event(
                title=event_data['title'],
                description=event_data['description'],
                event_date=event_data['event_date'],
                start_time=datetime.now().time(),  # Текущее время как время начала
                city=event_data['city'],
                location=event_data['location'],
                genre=event_data['genre'],
                ticket_price=event_data['ticket_price'],
                available_tickets=random.randint(10, 100),
                source='test_command',
                is_imported=False
            )
            event.save()
            created_count += 1
            self.stdout.write(self.style.SUCCESS(f'Создано мероприятие: {event.title}'))
        
        self.stdout.write(self.style.SUCCESS(f'Успешно добавлено {created_count} тестовых мероприятий!')) 