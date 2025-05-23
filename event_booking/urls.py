# event_booking/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from events import views as event_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('contacts/', event_views.contacts, name='contacts'),
    path('booked/', event_views.booked, name='booked'),
    path('', include('events.urls', namespace='events')),
    path('', include('booking.urls', namespace='booking')),
    path('users/', include(('users.urls', 'users'), namespace='users')),
    path('bot_api/', include('bot_api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
