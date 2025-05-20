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
        widget=forms.SelectMultiple(attrs={'class': 'select2 form-control'})#,
        #empty_label='Все жанры'
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
        # Добавляем пустую опцию в список выбора для городов и жанров
        self.fields['cities'].choices = [('', 'Все города')] + [
            (obj.pk, str(obj)) for obj in self.fields['cities'].queryset
        ]
        self.fields['genres'].choices = [('', 'Все жанры')] + [
            (obj.pk, str(obj)) for obj in self.fields['genres'].queryset
        ]