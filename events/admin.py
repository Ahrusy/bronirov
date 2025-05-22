from django.contrib import admin
from .models import Event, City, Location, Genre

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'address')
    list_filter = ('city',)
    search_fields = ('name', 'address')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'start_time', 'city', 'location', 'genre', 'ticket_price', 'available_tickets')
    list_filter = ('event_date', 'city', 'genre', 'is_imported')
    search_fields = ('title', 'description')
    date_hierarchy = 'event_date'
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'event_date', 'start_time')
        }),
        ('Место проведения', {
            'fields': ('city', 'location')
        }),
        ('Детали', {
            'fields': ('genre', 'ticket_price', 'available_tickets', 'rules')
        }),
        ('Медиа', {
            'fields': ('image', 'event_url')
        }),
        ('Метаданные', {
            'fields': ('external_id', 'source', 'is_imported', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
