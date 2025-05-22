from django import forms
from .models import City, Genre

class EventFilterForm(forms.Form):
    cities = forms.ModelChoiceField(
        queryset=City.objects.all(),
        required=False,
        empty_label='Все города',
        widget=forms.Select(attrs={'class': 'select2 form-control', 'style': 'width: 100%;'})
    )
    genres = forms.ModelChoiceField(
        queryset=Genre.objects.all(),
        required=False,
        empty_label='Все жанры',
        widget=forms.Select(attrs={'class': 'select2 form-control', 'style': 'width: 100%;'})
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Не добавляю пустую опцию вручную, select2 сам позволяет сбросить выбор