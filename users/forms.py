from django import forms
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils.crypto import get_random_string

class ProfileForm(forms.ModelForm):
    fullname = forms.CharField(label='ФИО', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', required=False, widget=forms.EmailInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))

    class Meta:
        model = UserProfile
        fields = ['fullname', 'email', 'phone', 'telegram_chat_id']
        labels = {
            'fullname': 'ФИО',
            'email': 'Email',
            'phone': 'Телефон',
            'telegram_chat_id': 'Telegram ID',
        }
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'telegram_chat_id': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CustomUserCreationForm(UserCreationForm):
    fullname = forms.CharField(label='ФИО', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label='Телефон', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def clean(self):
        cleaned_data = super().clean()
        from django.utils.crypto import get_random_string
        cleaned_data['username'] = get_random_string(10)
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(forms.Form):
    login = forms.CharField(label='Email или телефон', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        login = cleaned_data.get('login')
        password = cleaned_data.get('password')
        if login and password:
            self.user = authenticate(username=login, password=password)
            if self.user is None:
                raise forms.ValidationError('Неверный email/телефон или пароль.')
        return cleaned_data

    def get_user(self):
        return getattr(self, 'user', None)
