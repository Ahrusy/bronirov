# bookings/models.py
from django.db import models
from django.conf import settings
from events.models import Event
from django.utils import timezone

class BookingStatus(models.TextChoices):
    BOOKED = 'BOOKED', 'Забронировано'
    CANCELLED = 'CANCELLED', 'Отменено'
    CONFIRMED = 'CONFIRMED', 'Подтверждено'

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings', null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bookings')
    user_name = models.CharField(max_length=100, verbose_name='Имя')
    user_email = models.EmailField(verbose_name='Email')
    user_telegram = models.CharField(max_length=100, verbose_name='Telegram', blank=True, null=True)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=BookingStatus.choices, default=BookingStatus.BOOKED)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user_name} → {self.event.title} [{self.status}]"

    class Meta:
        unique_together = ('user', 'event')
        ordering = ['-booking_date']

class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Ожидает оплаты'),
        ('completed', 'Оплачено'),
        ('failed', 'Ошибка оплаты'),
        ('refunded', 'Возвращено'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('card', 'Банковская карта'),
        ('bank_transfer', 'Банковский перевод'),
    ]

    booking = models.OneToOneField('Booking', on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_id = models.CharField(max_length=100, unique=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='card')
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment_date = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ['-created_at']

    def __str__(self):
        return f'Платеж {self.payment_id} - {self.amount} руб.'

    def mark_as_completed(self):
        self.status = 'completed'
        self.payment_date = timezone.now()
        self.save()

    def mark_as_failed(self, error_message):
        self.status = 'failed'
        self.error_message = error_message
        self.save()

    def mark_as_refunded(self):
        self.status = 'refunded'
        self.save()

