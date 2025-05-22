from django.contrib import admin
from .models import Booking, Payment

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'user_email', 'event', 'booking_date', 'status', 'is_confirmed')
    list_filter = ('status', 'is_confirmed', 'booking_date')
    search_fields = ('user_name', 'user_email', 'user_telegram', 'event__title')
    date_hierarchy = 'booking_date'
    readonly_fields = ('booking_date',)
    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'event')
        }),
        ('Контактная информация', {
            'fields': ('user_name', 'user_email', 'user_telegram')
        }),
        ('Статус', {
            'fields': ('status', 'is_confirmed')
        }),
        ('Даты', {
            'fields': ('booking_date',)
        }),
    )

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'booking', 'amount', 'payment_method', 'status', 'created_at', 'payment_date')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('payment_id', 'booking__user_name', 'booking__user_email')
    readonly_fields = ('created_at', 'updated_at', 'payment_date')
    fieldsets = (
        ('Основная информация', {
            'fields': ('booking', 'amount', 'payment_id', 'payment_method')
        }),
        ('Статус', {
            'fields': ('status', 'error_message')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at', 'payment_date')
        }),
    )
