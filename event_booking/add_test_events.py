import os
import django
from datetime import datetime, timedelta

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_booking.settings')
django.setup()

from events.models import Event

# Очистка существующих мероприятий
Event.objects.all().delete()

# Создание тестовых мероприятий
events = [
    {
        'title': 'Рок-фестиваль "Лето в городе"',
        'description': 'Грандиозный рок-фестиваль с участием лучших российских и зарубежных групп. Три дня музыки, драйва и отличного настроения!',
        'event_date': datetime.now().date() + timedelta(days=30),
        'start_time': datetime.strptime('18:00', '%H:%M').time(),
        'location': 'Центральный парк',
        'city': 'Москва',
        'genre': 'Рок',
        'ticket_price': 3000.00,
        'available_tickets': 1000,
        'rules': 'Запрещено проносить алкоголь и еду. Возрастное ограничение: 18+',
        'event_url': 'https://example.com/rock-festival',
        'source': 'Организатор'
    },
    {
        'title': 'Выставка современного искусства',
        'description': 'Крупнейшая выставка современного искусства с работами известных художников и скульпторов. Интерактивные инсталляции и мастер-классы.',
        'event_date': datetime.now().date() + timedelta(days=15),
        'start_time': datetime.strptime('10:00', '%H:%M').time(),
        'location': 'Галерея современного искусства',
        'city': 'Санкт-Петербург',
        'genre': 'Искусство',
        'ticket_price': 1500.00,
        'available_tickets': 200,
        'rules': 'Фотосъемка разрешена без вспышки. Дети до 7 лет бесплатно.',
        'event_url': 'https://example.com/art-exhibition',
        'source': 'Галерея'
    },
    {
        'title': 'Театральный фестиваль "Маска"',
        'description': 'Ежегодный театральный фестиваль с участием лучших театров страны. Спектакли, мастер-классы и встречи с актерами.',
        'event_date': datetime.now().date() + timedelta(days=45),
        'start_time': datetime.strptime('19:00', '%H:%M').time(),
        'location': 'Городской театр',
        'city': 'Казань',
        'genre': 'Театр',
        'ticket_price': 2500.00,
        'available_tickets': 500,
        'rules': 'Дресс-код: вечерний. Дети до 12 лет не допускаются.',
        'event_url': 'https://example.com/theater-festival',
        'source': 'Театр'
    }
]

# Добавление мероприятий в базу данных
for event_data in events:
    Event.objects.create(**event_data)

print('Тестовые мероприятия успешно добавлены!') 