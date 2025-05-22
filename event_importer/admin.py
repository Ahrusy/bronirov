from django.contrib import admin
from .models import EventSource, ImportLog

# Register your models here.
admin.site.register(EventSource)
admin.site.register(ImportLog)
