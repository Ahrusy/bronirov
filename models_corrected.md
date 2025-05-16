``` python
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class City(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Название города

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"

    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=200)  # Название места (например, "Концертный зал")
    address = models.CharField(max_length=200)  # Адрес
    city = models.ForeignKey(City, on_delete=models.PROTECT, related_name='locations')  # Город
    postal_code = models.CharField(max_length=20, blank=True, null=True)  # Почтовый индекс (опционально)

    class Meta:
        verbose_name = "Место проведения"
        verbose_name_plural = "Места проведения"

    def __str__(self):
        return f"{self.name}, {self.city.name}"

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Название жанра (например, "Концерт")

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=200)  # Название мероприятия
    description = models.TextField(blank=True)  # Описание
    event_date = models.DateField()  # Дата проведения
    start_time = models.TimeField(blank=True, null=True)  # Время начала (опционально)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='events')  # Место проведения
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT, related_name='events')  # Жанр
    ticket_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0.0)]
    )  # Цена билета
    available_tickets = models.PositiveIntegerField(default=100)  # Остаток билетов
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)  # Афиша
    rules = models.TextField(blank=True, null=True)  # Правила посещения
    event_url = models.URLField(blank=True, null=True)  # Внешняя ссылка
    source = models.CharField(max_length=50, blank=True, null=True)  # Источник данных

    class Meta:
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"

    def __str__(self):
        return f"{self.title} ({self.event_date})"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')  # Пользователь
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bookings')  # Мероприятие
    booking_date = models.DateTimeField(auto_now_add=True)  # Дата бронирования
    is_cancelled = models.BooleanField(default=False)  # Статус отмены
    cancellation_date = models.DateTimeField(blank=True, null=True)  # Дата отмены (если отменено)

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        constraints = [
            models.UniqueConstraint(fields=['user', 'event'], name='unique_user_event_booking')
        ]

    def __str__(self):
        return f"Бронирование {self.user.username} на {self.event.title}"
```