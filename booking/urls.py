# bookings/urls.py
from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('book/<int:event_id>/', views.book_event, name='book_event'),
]
