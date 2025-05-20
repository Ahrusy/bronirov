# events/models.py
from django.db import models

# 🔹 Справочник городов
class City(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# 🔹 Справочник жанров (категорий)
class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# 🔹 Места проведения (связаны с городами)
class Location(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='locations')

    def __str__(self):
        return f"{self.name}, {self.city.name}"


# 🔹 Основная модель мероприятия
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    event_date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)

    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)

    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    available_tickets = models.PositiveIntegerField(default=100)

    rules = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)
    event_url = models.URLField(blank=True, null=True)

    # 🛰️ Поддержка импорта
    external_id = models.CharField(max_length=100, blank=True, null=True, unique=True)
    source = models.CharField(max_length=50, default='manual')
    is_imported = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['event_date', 'start_time']

    def __str__(self):
        return f"{self.title} ({self.event_date})"
