# events/views.py
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Event
from .forms import EventFilterForm
import bleach
from datetime import date, timedelta
from django.db.models import Q

def event_list(request):
    view_type = request.GET.get('view', request.session.get('view_type', 'card'))
    if view_type in ['card', 'list']:
        request.session['view_type'] = view_type
    else:
        view_type = 'card'

    today = date.today()
    week_later = today + timedelta(days=7)

    # Базовый QuerySet с фильтрами
    base_qs = Event.objects.select_related('city', 'location', 'genre')
    form = EventFilterForm(request.GET or None)
    if form.is_valid():
        cities = form.cleaned_data.get('cities')
        genres = form.cleaned_data.get('genres')
        date_from = form.cleaned_data.get('date_from')
        date_to = form.cleaned_data.get('date_to')

        if cities:
            if hasattr(cities, '__iter__') and not isinstance(cities, str):
                base_qs = base_qs.filter(city__in=cities)
            else:
                base_qs = base_qs.filter(city=cities)
        if hasattr(genres, '__iter__') and not isinstance(genres, str):
            base_qs = base_qs.filter(genre__in=genres)
        else:
            base_qs = base_qs.filter(genre=genres)
        if date_from and date_to:
            base_qs = base_qs.filter(event_date__range=(date_from, date_to))
        elif date_from:
            base_qs = base_qs.filter(event_date__gte=date_from)
        elif date_to:
            base_qs = base_qs.filter(event_date__lte=date_to)

    # Категории мероприятий (без фильтра по дате, только limit=7)
    upcoming_events = base_qs.order_by('event_date')[:7]
    free_events = base_qs.filter(
        (Q(ticket_price=0) | Q(ticket_price__isnull=True)) &
        (Q(price_text__isnull=True) | Q(price_text__exact='') | Q(price_text__iexact='Бесплатно'))
    ).order_by('event_date')[:7]
    paid_events = base_qs.filter(ticket_price__gt=0).order_by('event_date')[:7]
    finished_events = base_qs.filter(event_date__lt=today).order_by('-event_date')

    # Общий список событий с пагинацией
    events = base_qs.order_by('event_date')
    paginator = Paginator(events, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_title': 'Афиша мероприятий',
        'page_description': 'Бронируйте билеты на концерты, выставки, мастер-классы и другие события онлайн. Удобный поиск, фильтры и мгновенное подтверждение!',
        'upcoming_events': upcoming_events,
        'free_events': free_events,
        'paid_events': paid_events,
        'finished_events': finished_events,
        'form': form,
        'view_type': view_type,
        'events': page_obj,
        'is_paginated': page_obj.has_other_pages(),
    }

    return render(request, 'events/event_list.html', context=context)

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'events/event_detail.html', {'event': event})

def contacts(request):
    return render(request, 'events/contacts.html')

def booked(request):
    bookings = None
    if request.user.is_authenticated:
        bookings = request.user.bookings.select_related('event', 'event__city', 'event__location').all()
    return render(request, 'events/booked.html', {'bookings': bookings})
