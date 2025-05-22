# bookings/urls.py
from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('event/<int:event_id>/book/', views.book_event, name='book_event'),
    path('admin/', views.bookings_list, name='bookings_list'),
]
