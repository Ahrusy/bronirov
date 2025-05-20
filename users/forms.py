from django import forms
from .models import UserProfile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'telegram_chat_id']
        labels = {
            'phone': 'Телефон',
            'telegram_chat_id': 'Telegram ID',
        }
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'telegram_chat_id': forms.TextInput(attrs={'class': 'form-control'}),
        }
