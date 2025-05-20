# events/views.py
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Event
from .forms import EventFilterForm
import bleach

def event_list(request):
    view_type = request.GET.get('view', request.session.get('view_type', 'card'))
    if view_type in ['card', 'list']:
        request.session['view_type'] = view_type
    else:
        view_type = 'card'

    events = Event.objects.all().order_by('event_date')
    for event in events:
        event.description = bleach.clean(
            event.description,
            tags=[],
            attributes=[],
            strip=True
        )
    form = EventFilterForm(request.GET or None)
    cities = [city for city in request.GET.getlist('cities') if city]
    genres = [genre for genre in request.GET.getlist('genres') if genre]
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    if cities:
        try:
            cities = [int(city) for city in cities]
            events = events.filter(location__city__id__in=cities)
        except (ValueError, TypeError):
            pass  # Игнорируем невалидные ID городов
    if genres:
        try:
            genres = [int(genre) for genre in genres]
            events = events.filter(genre__id__in=genres)
        except (ValueError, TypeError):
            pass  # Игнорируем невалидные ID жанров
    if date_from:
        try:
            events = events.filter(event_date__gte=date_from)
        except ValueError:
            pass  # Игнорируем невалидный формат даты
    if date_to:
        try:
            events = events.filter(event_date__lte=date_to)
        except ValueError:
            pass  # Игнорируем невалидный формат даты



    # view_type = request.GET.get('view', 'card')  # По умолчанию карточки
    # if view_type not in ['card', 'table']:
    #     view_type = 'card'

    paginator = Paginator(events, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_title': 'Главная страница',
        'page_description': 'Добро пожаловать на наш сайт! Здесь вы найдете много полезной информации мероприятиях и не только.',
        'events': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'form': form,
        'view_type': view_type,
    }

    return render(request, 'events/event_list.html', context=context)

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'events/event_detail.html', {'event': event})
