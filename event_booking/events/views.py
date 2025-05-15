from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Event, Booking

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
    
    # Получаем уникальные значения для фильтров
    genres = Event.objects.values_list('genre', flat=True).distinct()
    cities = Event.objects.values_list('city', flat=True).distinct()
    
    # Пагинация
    paginator = Paginator(events, 6)  # 6 мероприятий на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'events': page_obj,
        'genres': genres,
        'cities': cities,
        'is_paginated': page_obj.has_other_pages(),
    }
    return render(request, 'events/event_list.html', context)

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'events/event_detail.html', {'event': event})

def book_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == 'POST':
        # Временная логика для демонстрации
        booking = Booking.objects.create(
            event=event,
            user_name=request.POST.get('user_name'),
            user_email=request.POST.get('user_email'),
            user_telegram=request.POST.get('user_telegram')
        )
        return render(request, 'events/booking_success.html', {
            'event': event,
            'booking': booking
        })
    
    return redirect('events:event_detail', pk=event_id) 