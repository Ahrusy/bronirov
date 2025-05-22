# bookings/urls.py
from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path('book/<int:event_id>/', views.book_event, name='book_event'),
    path('create/<int:event_id>/', views.create_booking, name='create_booking'),
    path('payment/<int:booking_id>/', views.process_payment, name='process_payment'),
    path('profile/', views.profile, name='profile'),
    path('booking/<int:booking_id>/', views.booking_detail, name='booking_detail'),
]
