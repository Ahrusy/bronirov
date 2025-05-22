from django.shortcuts import render, get_object_or_404
from .models import Event, Genre, City
from django.db.models import Q
from datetime import datetime, date

def event_list(request):
    events = Event.objects.select_related('genre', 'city', 'location').filter(is_imported=True).order_by('event_date')

    # Получаем параметры
    date_from = request.GET.get('date_from', '').strip()
    date_to = request.GET.get('date_to', '').strip()
    genre = request.GET.get('genre', '').strip()
    city = request.GET.get('city', '').strip()

    # Применяем фильтры, только если значения не пустые
    if date_from:
        try:
            date_obj = datetime.strptime(date_from, '%Y-%m-%d').date()
            events = events.filter(event_date__gte=date_obj)
        except ValueError:
            pass

    if date_to:
        try:
            date_obj = datetime.strptime(date_to, '%Y-%m-%d').date()
            events = events.filter(event_date__lte=date_obj)
        except ValueError:
            pass

    if genre:
        events = events.filter(genre__name__icontains=genre)

    if city:
        events = events.filter(city__name__icontains=city)

    genres = Genre.objects.all()
    cities = City.objects.all()

    return render(request, 'events/event_list.html', {
        'events': events,
        'genres': genres,
        'cities': cities,
        'filters': {
            'date_from': date_from,
            'date_to': date_to,
            'genre': genre,
            'city': city,
        }
    })

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'events/event_detail.html', {'event': event})
