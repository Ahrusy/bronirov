import pytest
from events.models import Event, Genre, City
from datetime import date, time


@pytest.mark.django_db
def test_event_creation():
    genre = Genre.objects.create(name='Концерт')
    city = City.objects.create(name='Москва')

    event = Event.objects.create(
        title='Test Event',
        description='Описание',
        event_date=date(2025, 6, 1),
        start_time=time(19, 0),
        location='Клуб XYZ',
        city=city,
        genre=genre,
        ticket_price=500,
        available_tickets=50
    )

    assert event.title == 'Test Event'
    assert event.city.name == 'Москва'
    assert event.genre.name == 'Концерт'
    assert event.available_tickets == 50
