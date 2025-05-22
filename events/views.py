# events/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Event, FavoriteEvent
from .forms import EventFilterForm
import bleach
from django.db import models
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse

def event_list(request):
    view_type = request.GET.get('view', request.session.get('view_type', 'card'))
    if view_type in ['card', 'list']:
        request.session['view_type'] = view_type
    else:
        view_type = 'card'

    events = Event.objects.all().order_by('event_date')

    # Поиск по мероприятиям
    query = request.GET.get('q', '').strip()
    if query:
        events = events.filter(
            models.Q(title__icontains=query) |
            models.Q(description__icontains=query) |
            models.Q(location__name__icontains=query)
        )

    # Пометка избранного для текущего пользователя
    favorite_ids = set()
    if request.user.is_authenticated:
        favorite_ids = set(FavoriteEvent.objects.filter(user=request.user).values_list('event_id', flat=True))
    for event in events:
        event.description = bleach.clean(
            event.description,
            tags=[],
            attributes=[],
            strip=True
        )
        event.is_favorite = event.id in favorite_ids
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

    sort = request.GET.get('sort')
    if sort == 'date':
        events = events.order_by('event_date')
    elif sort == 'price':
        events = events.order_by('ticket_price')
    elif sort == 'title':
        events = events.order_by('title')

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
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = FavoriteEvent.objects.filter(user=request.user, event=event).exists()
    return render(request, 'events/event_detail.html', {
        'event': event,
        'is_favorite': is_favorite
    })

@login_required
def toggle_favorite(request, event_id):
    if request.method == 'POST':
        event = get_object_or_404(Event, id=event_id)
        favorite = FavoriteEvent.objects.filter(user=request.user, event=event)
        
        if favorite.exists():
            favorite.delete()
            is_favorite = False
        else:
            FavoriteEvent.objects.create(user=request.user, event=event)
            is_favorite = True
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'is_favorite': is_favorite,
                'event_id': event_id
            })
        
        return redirect('events:event_detail', pk=event_id)
    return redirect('events:event_detail', pk=event_id)

@login_required
def favorite_events(request):
    favorites = FavoriteEvent.objects.filter(user=request.user).select_related('event')
    events = [fav.event for fav in favorites]
    return render(request, 'events/favorite_events.html', {'events': events})
