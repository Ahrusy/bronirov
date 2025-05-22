# events/urls.py
from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('event/<int:pk>/', views.event_detail, name='event_detail'),
    path('favorite/<int:event_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.favorite_events, name='favorite_events'),
]
