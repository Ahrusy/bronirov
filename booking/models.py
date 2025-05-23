# bookings/models.py
from django.db import models
from django.conf import settings
from events.models import Event

class BookingStatus(models.TextChoices):
    BOOKED = 'BOOKED', 'Забронировано'
    CANCELLED = 'CANCELLED', 'Отменено'
    CONFIRMED = 'CONFIRMED', 'Подтверждено'

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings', null=True, blank=True, verbose_name='Пользователь')
    user_name = models.CharField(max_length=100, verbose_name='Имя посетителя', blank=True, null=True)
    user_email = models.EmailField(verbose_name='Email', blank=True, null=True)
    user_telegram = models.CharField(max_length=100, blank=True, null=True, verbose_name='Telegram (username)')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата бронирования')
    status = models.CharField(max_length=20, choices=BookingStatus.choices, default=BookingStatus.BOOKED)
    is_confirmed = models.BooleanField(default=False)
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество билетов')

    def __str__(self):
        if self.user:
            return f"{self.user.username} → {self.event.title} [{self.status}]"
        return f"{self.user_name or self.user_email} → {self.event.title} [{self.status}]"

    class Meta:
        unique_together = (('user', 'event'),)
        ordering = ['-booking_date']

