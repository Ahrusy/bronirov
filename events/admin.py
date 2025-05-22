from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'location', 'genre', 'ticket_price')
    search_fields = ('title', 'location', 'genre')
    list_filter = ('genre', 'event_date')
