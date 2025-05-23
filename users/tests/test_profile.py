from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class ProfileViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='profileuser', password='Testpass123!')

    def test_profile_view_authenticated(self):
        self.client.login(username='profileuser', password='Testpass123!')
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'profileuser')

    def test_profile_view_unauthenticated(self):
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 302)  # редирект на login 