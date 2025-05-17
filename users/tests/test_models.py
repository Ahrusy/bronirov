import pytest
from django.contrib.auth.models import User
from users.models import UserProfile


@pytest.mark.django_db
def test_user_profile_created():
    user = User.objects.create_user(username='jake', password='secret')
    profile = user.profile  # ← профиль уже создан

    profile.telegram_chat_id = '123456'
    profile.save()

    assert profile.telegram_chat_id == '123456'
