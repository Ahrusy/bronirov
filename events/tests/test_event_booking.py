from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from events.models import Event, City, Location
from booking.models import Booking
from datetime import date

class EventBookingTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='booker', password='Testpass123!')
        self.city = City.objects.create(name='Test City', slug='test-city')
        self.location = Location.objects.create(name='Test Location', city=self.city)
        self.event = Event.objects.create(
            title='Test Event',
            event_date=date.today(),
            city=self.city,
            location=self.location,
        )

    def test_event_booking(self):
        self.client.login(username='booker', password='Testpass123!')
        response = self.client.post(reverse('booking:book_event', args=[self.event.pk]), {
            'user_name': 'Booker',
            'user_email': 'booker@example.com',
            'user_telegram': '@booker',
        })
        self.assertEqual(response.status_code, 302)  # редирект после успешного бронирования
        self.assertTrue(Booking.objects.filter(event=self.event, user_name='Booker').exists()) 