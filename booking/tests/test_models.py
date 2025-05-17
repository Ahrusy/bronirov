import pytest
from django.contrib.auth.models import User
from events.models import Event, Genre, City
from booking.models import Booking, BookingStatus
from datetime import date


@pytest.mark.django_db
def test_booking_unique_constraint():
    user = User.objects.create_user(username='hacker', password='secret')
    genre = Genre.objects.create(name='Выставка')
    city = City.objects.create(name='Питер')
    event = Event.objects.create(
        title='HackConf',
        event_date=date(2025, 7, 1),
        location='Expo',
        city=city,
        genre=genre,
        ticket_price=1000,
        available_tickets=10
    )

    booking1 = Booking.objects.create(user=user, event=event)
    assert booking1.status == BookingStatus.BOOKED

    with pytest.raises(Exception):
        Booking.objects.create(user=user, event=event)  # Уникальность по user+event
