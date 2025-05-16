# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    telegram = models.CharField(max_length=100, blank=True, null=True, verbose_name='Telegram username')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Телефон')

    def __str__(self):
        return self.username
