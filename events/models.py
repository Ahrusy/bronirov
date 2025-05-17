# events/models.py
from django.db import models

class City(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    event_date = models.DateField()
    start_time = models.TimeField(blank=True, null=True)
    location = models.CharField(max_length=200)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    available_tickets = models.PositiveIntegerField(default=100)
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    rules = models.TextField(blank=True, null=True)
    event_url = models.URLField(blank=True, null=True)
    source = models.CharField(max_length=50, blank=True, null=True)
    is_imported = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} ({self.event_date})"

    class Meta:
        ordering = ['event_date']

