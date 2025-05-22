from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['user_name', 'user_email', 'user_telegram']
        widgets = {
            'user_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'}),
            'user_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email для подтверждения'}),
            'user_telegram': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '@username (опционально)'}),
        } 