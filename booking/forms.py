from django import forms
from .models import Booking
 
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['quantity']
        labels = {'quantity': 'Количество билетов'}
        widgets = {'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 20})} 