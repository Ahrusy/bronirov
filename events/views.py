# events/views.py
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Event

def event_list(request):
    events = Event.objects.all().order_by('event_date')

    # Фильтрация
    search = request.GET.get('search', '')
    genre = request.GET.get('genre', '')
    city = request.GET.get('city', '')

    if search:
        events = events.filter(title__icontains=search)
    if genre:
        events = events.filter(genre=genre)
    if city:
        events = events.filter(city=city)

    genres = Event.objects.values_list('genre', flat=True).distinct()
    cities = Event.objects.values_list('city', flat=True).distinct()

    paginator = Paginator(events, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'events/event_list.html', {
        'events': page_obj,
        'genres': genres,
        'cities': cities,
        'is_paginated': page_obj.has_other_pages(),
    })

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'events/event_detail.html', {'event': event})
