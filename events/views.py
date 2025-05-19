# events/views.py
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Event
from .forms import EventFilterForm

def event_list(request):
    events = Event.objects.all().order_by('event_date')
    form = EventFilterForm(request.GET or None)

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
    if form.is_valid():
        cities = form.cleaned_data.get('cities')
        genres = form.cleaned_data.get('genres')
        date_from = form.cleaned_data.get('date_from')
        date_to = form.cleaned_data.get('date_to')

        if cities:
            events = events.filter(location__city__in=cities)
        if genres:
            events = events.filter(genre__in=genres)
        if date_from:
            events = events.filter(event_date__gte=date_from)
        if date_to:
            events = events.filter(event_date__lte=date_to)

    context = {
        'page_title': 'Главная страница',
        'page_description': 'Добро пожаловать на наш сайт! Здесь вы найдете много полезной информации.',
        'events': page_obj,
        'genres': genres,
        'cities': cities,
        'is_paginated': page_obj.has_other_pages(),
        'form': form,
    }

    return render(request, 'events/event_list.html', context=context)

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'events/event_detail.html', {'event': event})
