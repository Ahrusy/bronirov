from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class RegistrationLoginTest(TestCase):
    def test_register_user(self):
        response = self.client.post(reverse('users:register'), {
            'username': 'testuser',
            'password1': 'Testpass123!',
            'password2': 'Testpass123!',
        })
        self.assertEqual(response.status_code, 302)  # редирект после успешной регистрации
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_login_user(self):
        User.objects.create_user(username='testuser', password='Testpass123!')
        response = self.client.post(reverse('users:login'), {
            'username': 'testuser',
            'password': 'Testpass123!',
        })
        self.assertEqual(response.status_code, 302)  # редирект после успешного входа
        self.assertTrue('_auth_user_id' in self.client.session) 