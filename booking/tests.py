from django.test import TestCase
from .models import Booking
from events.models import Event
from django.utils import timezone

# Create your tests here.

class BookingModelTest(TestCase):
    def setUp(self):
        self.event = Event.objects.create(
            title="Test Event",
            event_date=timezone.now().date(),
            location=None,
            city=None,
            genre=None,
            ticket_price=10.00,
            available_tickets=2
        )
    def test_booking_creation(self):
        booking = Booking.objects.create(
            user_name="Test User",
            user_email="test@example.com",
            event=self.event
        )
        self.assertEqual(booking.user_name, "Test User")
        self.assertEqual(booking.event, self.event)
