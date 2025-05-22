import requests
import time
from datetime import datetime, timezone
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.db import transaction
from events.models import City, Location, Genre, Event
from django.utils import timezone as dj_timezone

class Command(BaseCommand):
    help = 'Import max 100 NEW events from KudaGo API, которые начинаются позже момента запуска скрипта (по московскому времени)'

    def handle(self, *args, **kwargs):
        BASE_URL = 'https://kudago.com/public-api/v1.4'

        self.stdout.write('🔹 Fetching genre mappings...')
        genre_map = {}
        genres_response = requests.get(f'{BASE_URL}/event-categories/?lang=ru')
        if genres_response.ok:
            for genre_data in genres_response.json():
                genre_map[genre_data['slug']] = genre_data['name']
        else:
            self.stdout.write(self.style.ERROR('Failed to fetch genre mappings'))
            return

        self.stdout.write('🔹 Caching cities...')
        city_cache = {}
        cities_response = requests.get(f'{BASE_URL}/locations/?lang=ru')
        if cities_response.ok:
            for city_data in cities_response.json():
                city, _ = City.objects.get_or_create(name=city_data['name'])
                city_cache[city.name.lower()] = city
        else:
            self.stdout.write(self.style.ERROR('Failed to fetch cities'))
            return

        self.stdout.write('🔹 Caching genres...')
        genre_cache = {}
        for slug, name in genre_map.items():
            genre, _ = Genre.objects.get_or_create(name=name)
            genre_cache[slug] = genre

        self.stdout.write('🚀 Importing max 100 NEW events (2024–2025)...')
        page = 1
        created_count = 0
        MAX_NEW_EVENTS = 100

        while created_count < MAX_NEW_EVENTS:
            response = requests.get(
                f'{BASE_URL}/events/',
                params={
                    'lang': 'ru',
                    'fields': 'id,title,description,dates,location,place,categories,price,images,body_text,site_url',
                    'page': page,
                    'page_size': 100
                }
            )
            if not response.ok:
                self.stdout.write(self.style.ERROR('Failed to fetch events'))
                break

            results = response.json().get('results', [])
            if not results:
                break

            with transaction.atomic():
                for data in results:
                    if created_count >= MAX_NEW_EVENTS:
                        break  # 💥 Прерываем импорт

                    # --- Начало блока обработки одного события ---
                    date_info = data.get('dates', [{}])[0]
                    start_ts = date_info.get('start')
                    if not isinstance(start_ts, (int, float)) or start_ts <= 0:
                        continue
                    if start_ts > 10**12:  # миллисекунды
                        start_ts = start_ts / 1000

                    # Получаем текущее время в Москве
                    now_msk = dj_timezone.localtime(dj_timezone.now())
                    self.stdout.write(self.style.WARNING(f'Время запуска скрипта (МСК): {now_msk.strftime("%Y-%m-%d %H:%M:%S")}'))
                    # dt — это datetime начала события (UTC)
                    dt = datetime.fromtimestamp(start_ts, tz=timezone.utc)
                    dt_msk = dt.astimezone(now_msk.tzinfo)
                    if dt_msk <= now_msk:
                        continue
                    event_date = dt.date()
                    start_time = dt.time()

                    if event_date.year < 2024 or event_date.year > 2025:
                        continue

                    city_name = data.get('location', {}).get('name', 'unknown').lower()
                    city = city_cache.get(city_name)
                    if not city:
                        city, _ = City.objects.get_or_create(name=city_name.title())
                        city_cache[city.name.lower()] = city

                    place_data = data.get('place') or {}
                    location_name = place_data.get('title', 'Unknown Place')
                    address = place_data.get('address', '')
                    postal_code = place_data.get('postal_code', '')
                    location, _ = Location.objects.get_or_create(
                        name=location_name,
                        address=address,
                        city=city,
                        defaults={'postal_code': postal_code}
                    )

                    slug = (data.get('categories') or ['other'])[0]
                    genre = genre_cache.get(slug)
                    if not genre:
                        genre, _ = Genre.objects.get_or_create(name=slug)
                        genre_cache[slug] = genre

                    price_raw = data.get('price', '')
                    try:
                        ticket_price = float(price_raw.split()[0].replace(',', '.')) if price_raw and price_raw[0].isdigit() else 0.00
                    except Exception:
                        ticket_price = 0.00

                    external_id = str(data.get('id'))

                    try:
                        event, created = Event.objects.get_or_create(
                            external_id=external_id,
                            defaults={
                                'title': data.get('title', 'Untitled'),
                                'description': data.get('description', ''),
                                'event_date': event_date,
                                'start_time': start_time,
                                'city': city,
                                'location': location,
                                'genre': genre,
                                'ticket_price': ticket_price,
                                'available_tickets': 100,
                                'rules': data.get('body_text', ''),
                                'event_url': data.get('site_url', ''),
                                'source': 'KudaGo',
                                'is_imported': True,
                            }
                        )
                        if created:
                            created_count += 1
                            self.stdout.write(self.style.SUCCESS(f'✅ Created [{created_count}]: {event.title}'))
                            # 🖼️ Загрузка изображения
                            images = data.get('images', [])
                            if images:
                                image_url = images[0].get('image', '')
                                if image_url:
                                    try:
                                        img_res = requests.get(image_url)
                                        if img_res.ok:
                                            file_name = f"event_{event.id}.jpg".replace(':', '-').replace(' ', '_')
                                            event.image.save(
                                                file_name,
                                                ContentFile(img_res.content),
                                                save=True
                                            )
                                    except Exception as img_err:
                                        self.stdout.write(self.style.WARNING(f"Image failed for {event.title}: {img_err}"))
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f"Ошибка при создании события: {e}"))
                    # --- Конец блока обработки одного события ---

            page += 1
            time.sleep(1)

        self.stdout.write(self.style.SUCCESS(f'🎉 Imported {created_count} new events (2024–2025). Done!'))
