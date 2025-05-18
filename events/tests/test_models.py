import pytest
from datetime import date, time

from events.models import City, Genre, Location, Event

@pytest.mark.django_db
def test_create_city():
    city = City.objects.create(name="Москва")
    assert str(city) == "Москва"

@pytest.mark.django_db
def test_create_genre():
    genre = Genre.objects.create(name="Концерт")
    assert str(genre) == "Концерт"

@pytest.mark.django_db
def test_create_location():
    city = City.objects.create(name="Санкт-Петербург")
    location = Location.objects.create(
        name="Главный зал",
        address="Невский проспект, 100",
        postal_code="190000",
        city=city
    )
    assert "Главный зал" in str(location)
    assert "Санкт-Петербург" in str(location)

@pytest.mark.django_db
def test_create_event_with_all_fields():
    city = City.objects.create(name="Казань")
    genre = Genre.objects.create(name="Выставка")
    location = Location.objects.create(
        name="Центр искусств",
        address="ул. Баумана, 1",
        city=city
    )

    event = Event.objects.create(
        title="Современное искусство",
        description="Экспозиция работ 2024",
        event_date=date(2025, 6, 15),
        start_time=time(18, 30),
        city=city,
        location=location,
        genre=genre,
        ticket_price=750.00,
        available_tickets=200,
        rules="Вход с 16+",
        image=None,
        event_url="https://example.com/art",
        external_id="kudago12345",
        source="kudago",
        is_imported=True
    )

    assert event.title == "Современное искусство"
    assert event.city.name == "Казань"
    assert event.genre.name == "Выставка"
    assert event.location.name == "Центр искусств"
    assert event.ticket_price == 750.00
    assert event.is_imported is True
    assert str(event) == "Современное искусство (2025-06-15)"
