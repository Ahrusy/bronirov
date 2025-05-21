from django.test import TestCase, Client
from users.models import User, UserProfile


class TelegramValidationTest(TestCase):
    def test_validation_success(self):
        user = User.objects.create(username="testuser")
        profile = UserProfile.objects.create(user=user, telegram_verification_token="abc123")

        c = Client()
        response = c.post("/api/telegram/validate/", data=json.dumps({
            "token": "abc123",
            "telegram_id": "12345678",
            "telegram_username": "test_bot"
        }), content_type="application/json")

        self.assertEqual(response.status_code, 200)
        profile.refresh_from_db()
        self.assertTrue(profile.is_telegram_verified)
