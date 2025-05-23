from booking.urls import app_name

app_name = 'pages'

from django.urls import path
from . import views

urlpatterns = [
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('sitemap/', views.sitemap, name='sitemap'),
]