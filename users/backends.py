from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from users.models import UserProfile

def normalize_phone(phone):
    return ''.join(c for c in phone if c.isdigit() or c == '+')

class EmailOrPhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, login=None, **kwargs):
        login = login or username
        user = None
        if login:
            login = login.strip()
            if '@' in login:
                # Поиск по email (берём первого найденного)
                user = User.objects.filter(email__iexact=login.lower()).first()
            else:
                # Поиск по телефону
                norm_phone = normalize_phone(login)
                profile = UserProfile.objects.filter(phone=norm_phone).first()
                if profile:
                    user = profile.user
        if user and user.check_password(password):
            return user
        return None 