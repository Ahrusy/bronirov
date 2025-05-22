from django.contrib import admin
from .models import Event, City, Genre, Location

# Register your models here.
admin.site.register(Event)
admin.site.register(City)
admin.site.register(Genre)
admin.site.register(Location)
