from django import forms
from .models import City, Genre

class EventFilterForm(forms.Form):
    cities = forms.ModelMultipleChoiceField(
        queryset=City.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'select2 form-control'})
    )
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'select2 form-control'})
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )