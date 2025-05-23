# users/models.py
from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    fullname = models.CharField(max_length=150, blank=True, null=True, verbose_name='ФИО')
    telegram_chat_id = models.CharField(max_length=50, blank=True, null=True)
    telegram_username = models.CharField(max_length=50, blank=True, null=True)
    is_telegram_verified = models.BooleanField(default=False)
    telegram_verified_at = models.DateTimeField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"Профиль {self.user.username}"

class TelegramConfirmation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='telegram_confirmation')
    token = models.CharField(max_length=64, unique=True, default=uuid.uuid4)
    is_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(blank=True, null=True)

    def mark_confirmed(self):
        self.is_confirmed = True
        self.confirmed_at = timezone.now()
        self.save()

    def __str__(self):
        return f"TelegramConfirmation({self.user.username}, confirmed={self.is_confirmed})"

