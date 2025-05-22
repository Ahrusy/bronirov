# bookings/models.py
from django.db import models
from django.conf import settings
from events.models import Event

class BookingStatus(models.TextChoices):
    BOOKED = 'BOOKED', 'Забронировано'
    CANCELLED = 'CANCELLED', 'Отменено'
    CONFIRMED = 'CONFIRMED', 'Подтверждено'

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=BookingStatus.choices, default=BookingStatus.BOOKED)
    is_confirmed = models.BooleanField(default=False)
    ticket_count = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} → {self.event.title} [{self.status}]"

    class Meta:
        unique_together = ('user', 'event')
        ordering = ['-booking_date']

