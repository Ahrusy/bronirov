import requests
import time
from datetime import datetime
from django.core.management.base import BaseCommand
import datetime
from django.core.files.base import ContentFile
from django.db import transaction
from events.models import City, Location, Genre, Event
import pytz
from collections import defaultdict
import calendar

# Определяем разумный диапазон дат
MIN_TIMESTAMP = 0  # 1970-01-01 (начало эпохи UNIX)
MAX_TIMESTAMP = 4102444800  # 2100-01-01

class Command(BaseCommand):
    help = 'Populate database with events from KudaGo API'

    def handle(self, *args, **kwargs):
        BASE_URL = 'https://kudago.com/public-api/v1.4'

        # Получаем соответствие slug → name для жанров
        self.stdout.write('Fetching genre mappings...')
        genres_response = requests.get(f'{BASE_URL}/event-categories/?lang=ru')
        genre_map = {}
        if genres_response.status_code == 200:
            genres = genres_response.json()
            for genre_data in genres:
                genre_map[genre_data['slug']] = genre_data['name']
            self.stdout.write(self.style.SUCCESS('Genre mapping loaded.'))
        else:
            self.stdout.write(self.style.ERROR('Failed to fetch genre mappings'))
            return

        # Загружаем города
        self.stdout.write('Populating cities...')
        cities_response = requests.get(f'{BASE_URL}/locations/')
        if cities_response.status_code == 200:
            cities = cities_response.json()
            cities.append({'slug': 'online', 'name': 'Online'})
            for city_data in cities:
                city,created = City.objects.get_or_create(
                    slug=city_data['slug'],
                    defaults={'name': city_data['name']},
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Создан город: {city.name} ({city.slug})'))
                else:
                    self.stdout.write(f'Город уже существует: {city.name} ({city.slug})')

            self.stdout.write(self.style.SUCCESS(f'Successfully populated {len(cities)} cities'))
        else:
            self.stdout.write(self.style.ERROR('Failed to fetch cities'))

        # Загружаем жанры (если потребуется)
        self.stdout.write('Populating genres...')
        for slug, name in genre_map.items():
            Genre.objects.get_or_create(name=name)
        self.stdout.write(self.style.SUCCESS(f'Successfully populated {len(genre_map)} genres'))

        # Загружаем события
        self.stdout.write('Populating events...')
        page = 1
        while True:
            tz=pytz.timezone('Europe/Moscow')
            current_time = datetime.datetime.now(tz).astimezone(pytz.UTC)
            unix_timestamp = int(current_time.timestamp())
            events_response = requests.get(
                f'{BASE_URL}/events/',
                params={
                    'lang': 'ru',
                    'fields': 'id,title,description,dates,location,place,categories,price,images,body_text,site_url',
                    'page': page,
                    'page_size': 100,
                    'actual_since': unix_timestamp,
                }
            )
            if events_response.status_code != 200:
                self.stdout.write(self.style.ERROR('Failed to fetch events'))
                break

            events_data = events_response.json()
            results = events_data.get('results', [])
            if not results:
                break  # Нет больше событий

            for event_data in results:
                try:
                    # Получение города
                    city_name = event_data.get('location', {}).get('slug', 'Unknown')
                    city, _ = City.objects.get_or_create(slug=city_name)

                    # Получение места проведения
                    place_data = event_data.get('place') or {}
                    place_name = place_data.get('title', 'Unknown Place')
                    place_address = place_data.get('address', '')
                    postal_code = place_data.get('postal_code', '')
                    location, _ = Location.objects.get_or_create(
                        name=place_name,
                        city=city,
                        defaults={
                            'address': place_address,
                            'postal_code': postal_code,
                        }
                    )

                    # Получение жанра (берём первый slug, ищем название)
                    category_slug = (event_data.get('categories') or ['other'])[0]
                    category_name = genre_map.get(category_slug, category_slug)
                    genre, _ = Genre.objects.get_or_create(name=category_name)

                    # Обработка даты и времени
                    dates = (event_data.get('dates') or [{}])
                    # Найти ближайшую будущую дату
                    event_date = None
                    start_time = None
                    now_ts = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
                    min_future_ts = None
                    for d in dates:
                        start_ts = d.get('start', 0)
                        if start_ts > now_ts:
                            if min_future_ts is None or start_ts < min_future_ts:
                                min_future_ts = start_ts
                    if min_future_ts:
                        start_date = datetime.datetime.fromtimestamp(min_future_ts, tz=datetime.timezone.utc)
                        event_date = start_date.date()
                        start_time = start_date.time()
                    else:
                        # Если нет будущих дат, пробуем взять первую валидную дату
                        for d in dates:
                            start_ts = d.get('start', 0)
                            if start_ts > 0:
                                start_date = datetime.datetime.fromtimestamp(start_ts, tz=datetime.timezone.utc)
                                event_date = start_date.date()
                                start_time = start_date.time()
                                break
                    if not event_date:
                        continue  # пропускать события без даты

                    # Обработка цены
                    price = event_data.get('price', '')
                    try:
                        ticket_price = float(price.split()[0].replace(',', '.')) if price and price[0].isdigit() else 0.00
                    except (ValueError, IndexError):
                        ticket_price = 0.00
                    price_text = price if price else None

                    # Получение external_id
                    external_id = str(event_data.get('id'))

                    # Получение текстового расписания (schedule_text)
                    # Исправлено: сохраняем только ближайший актуальный диапазон дат и времени
                    schedule_text = event_data.get('when')
                    if not schedule_text:
                        # Если нет 'when', ищем ближайшую будущую дату/диапазон
                        future_dates = [d for d in dates if d.get('start', 0) > now_ts]
                        if future_dates:
                            # Берём ближайший диапазон
                            d = min(future_dates, key=lambda x: x.get('start', 0))
                            start_dt = datetime.datetime.fromtimestamp(d['start'], tz=datetime.timezone.utc)
                            end_dt = datetime.datetime.fromtimestamp(d['end'], tz=datetime.timezone.utc) if d.get('end') else None
                            if end_dt and start_dt.date() != end_dt.date():
                                # Диапазон дат
                                schedule_text = f"{start_dt.strftime('%d.%m.%Y')} – {end_dt.strftime('%d.%m.%Y')} {start_dt.strftime('%H:%M')}–{end_dt.strftime('%H:%M')}"
                            else:
                                # Одна дата
                                schedule_text = f"{start_dt.strftime('%d.%m.%Y')} {start_dt.strftime('%H:%M')}–{end_dt.strftime('%H:%M') if end_dt else ''}"
                        else:
                            # Если нет будущих дат, fallback: первая валидная дата
                            for d in dates:
                                if d.get('start', 0) > 0:
                                    start_dt = datetime.datetime.fromtimestamp(d['start'], tz=datetime.timezone.utc)
                                    end_dt = datetime.datetime.fromtimestamp(d['end'], tz=datetime.timezone.utc) if d.get('end') else None
                                    if end_dt and start_dt.date() != end_dt.date():
                                        schedule_text = f"{start_dt.strftime('%d.%m.%Y')} – {end_dt.strftime('%d.%m.%Y')} {start_dt.strftime('%H:%M')}–{end_dt.strftime('%H:%M')}"
                                    else:
                                        schedule_text = f"{start_dt.strftime('%d.%m.%Y')} {start_dt.strftime('%H:%M')}–{end_dt.strftime('%H:%M') if end_dt else ''}"
                                    break

                    # Формирование заголовка с возрастным ограничением
                    title = event_data.get('title', 'Untitled')
                    age = event_data.get('age_restriction')
                    if age:
                        title = f"{title} {age}+"
                    # Название с заглавной буквы
                    if title:
                        title = title[:1].upper() + title[1:]

                    # Описание без дублирующегося титула
                    description = event_data.get('description', '')
                    if description and title and description.lower().startswith(title.lower()):
                        description = description[len(title):].lstrip(' .,-–—')

                    event, created = Event.objects.get_or_create(
                        external_id=external_id,
                        defaults={
                            'title': title,
                            'description': description,
                            'event_date': event_date,
                            'start_time': start_time,
                            'city': city,
                            'location': location,
                            'genre': genre,
                            'ticket_price': ticket_price,
                            'price_text': price_text,
                            'available_tickets': 100,
                            'rules': event_data.get('body_text', ''),
                            'image': None,
                            'event_url': event_data.get('site_url', ''),
                            'source': 'KudaGo',
                            'is_imported': True,
                            'schedule_text': schedule_text,
                        }
                    )

                    # Обновление изображения (если есть в KudaGo)
                    images = event_data.get('images', [])
                    if images:
                        image_url = images[0].get('image', '')
                        if image_url:
                            try:
                                image_response = requests.get(image_url)
                                if image_response.status_code == 200:
                                    event.image.save(
                                        f"event_{event.id}.jpg",
                                        ContentFile(image_response.content),
                                        save=True
                                    )
                            except requests.RequestException:
                                self.stdout.write(self.style.WARNING(f'Failed to download image for event {event.title}'))

                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Created event: {event.title}'))
                    else:
                        self.stdout.write(f'Event already exists: {event.title}')
                    time.sleep(0.1)  # Пауза между событиями
                except City.DoesNotExist:
                    self.stdout.write(f"Город с slug '{city_name}' не найден. Пропускаем событие: {event_data.get('title', 'Unknown')}")
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error processing event {event_data.get("title")}: {str(e)}'))

            page += 1
            time.sleep(1)  # Пауза для избежания лимитов API

        self.stdout.write(self.style.SUCCESS('Finished populating events'))
