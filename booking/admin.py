from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'user_email', 'event', 'booking_date', 'status')
    search_fields = ('user_name', 'user_email', 'user_telegram')
    list_filter = ('event', 'status', 'booking_date')
