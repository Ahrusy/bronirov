from django import forms
from .models import Booking
 
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['user_name', 'user_email', 'user_telegram'] 