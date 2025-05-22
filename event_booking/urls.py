# event_booking/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('events.urls', namespace='events')),
    path('booking/', include('booking.urls', namespace='booking')),
    path('users/', include('users.urls')),
    path('api/', include('bot_api.urls')),  # например, http://localhost:8000/api/telegram/validate/
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
