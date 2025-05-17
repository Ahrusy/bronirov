from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

'''
@receiver(post_save, sender=User)	Слушает событие "после сохранения" модели User
created	Булевый флаг, указывает: объект создан (True) или обновлён
UserProfile.objects.create(user=instance)	Создаёт профиль для нового пользователя

🔁 Это обеспечивает автоматическое создание UserProfile сразу после регистрации пользователя.
'''

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)
