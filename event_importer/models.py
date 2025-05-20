# event_importer/models.py
from django.db import models

class EventSource(models.Model):
    name = models.CharField(max_length=100)
    source_type = models.CharField(max_length=50, choices=[('rss', 'RSS'), ('api', 'API'), ('html', 'HTML')])
    url = models.URLField()
    last_checked = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

class ImportLog(models.Model):
    source = models.ForeignKey(EventSource, on_delete=models.CASCADE, related_name='logs')
    raw_data = models.TextField()
    status = models.CharField(max_length=20, choices=[('success', 'Успешно'), ('fail', 'Ошибка')])
    error_message = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.source.name} @ {self.timestamp}"
