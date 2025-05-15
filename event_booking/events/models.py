from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    event_date = models.DateField(verbose_name='Дата проведения')
    start_time = models.TimeField(blank=True, null=True, verbose_name='Время начала')
    location = models.CharField(max_length=200, verbose_name='Место проведения')
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name='Город')
    genre = models.CharField(max_length=100, verbose_name='Жанр')
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена билета')
    available_tickets = models.PositiveIntegerField(default=100, verbose_name='Доступно билетов')
    image = models.ImageField(upload_to='event_images/', blank=True, null=True, verbose_name='Изображение')
    rules = models.TextField(blank=True, null=True, verbose_name='Правила посещения')
    event_url = models.URLField(blank=True, null=True, verbose_name='Ссылка на страницу мероприятия')
    source = models.CharField(max_length=50, blank=True, null=True, verbose_name='Источник')

    def __str__(self):
        return f"{self.title} ({self.event_date})"

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'
        ordering = ['event_date']

class Booking(models.Model):
    user_name = models.CharField(max_length=100, verbose_name='Имя посетителя')
    user_email = models.EmailField(verbose_name='Email')
    user_telegram = models.CharField(max_length=100, blank=True, null=True, verbose_name='Telegram (username)')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bookings', verbose_name='Мероприятие')
    booking_date = models.DateField(auto_now_add=True, verbose_name='Дата бронирования')

    def __str__(self):
        return f"{self.user_name} - {self.event.title} ({self.booking_date})"

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'
        ordering = ['-booking_date'] 