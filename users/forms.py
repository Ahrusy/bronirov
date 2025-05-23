from django import forms
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username',)
