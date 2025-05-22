# bookings/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Booking
from events.models import Event
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
import requests
from django.db import transaction
from django.contrib.admin.views.decorators import staff_member_required
from django import forms

@login_required
def book_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if event.available_tickets <= 0:
        messages.error(request, 'Билеты на это мероприятие закончились.')
        return redirect('events:event_detail', pk=event_id)

    class TicketForm(forms.Form):
        ticket_count = forms.IntegerField(min_value=1, max_value=event.available_tickets, initial=1)

    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket_count = form.cleaned_data['ticket_count']
            with transaction.atomic():
                event = Event.objects.select_for_update().get(id=event_id)
                if event.available_tickets < ticket_count:
                    messages.error(request, 'Недостаточно билетов.')
                    return redirect('events:event_detail', pk=event_id)
                if Booking.objects.filter(event=event, user=request.user).exists():
                    messages.error(request, 'Вы уже бронировали это мероприятие.')
                    return redirect('events:event_detail', pk=event_id)
                booking = Booking.objects.create(
                    event=event,
                    user=request.user,
                    ticket_count=ticket_count
                )
                event.available_tickets -= ticket_count
                event.save(update_fields=["available_tickets"])
                messages.success(request, 'Бронирование успешно выполнено!')
                # Отправка email
                if request.user.email:
                    send_mail(
                        subject=f'Бронирование мероприятия: {event.title}',
                        message=f'Вы успешно забронировали билет на "{event.title}" ({event.event_date})',
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[request.user.email],
                        fail_silently=True
                    )
                # Отправка уведомления в Telegram
                profile = getattr(request.user, 'profile', None)
                if profile and profile.telegram_chat_id:
                    token = getattr(settings, 'TELEGRAM_BOT_TOKEN', None)
                    chat_id = profile.telegram_chat_id
                    if token and chat_id:
                        text = f'Вы успешно забронировали билет на "{event.title}" ({event.event_date})'
                        url = f'https://api.telegram.org/bot{token}/sendMessage'
                        requests.post(url, data={'chat_id': chat_id, 'text': text})
                return render(request, 'booking/booking_success.html', {
                    'event': event,
                    'booking': booking
                })
        else:
            messages.error(request, 'Ошибка в количестве билетов.')
    else:
        form = TicketForm()
    return render(request, 'booking/book_event.html', {'event': event, 'form': form})

@staff_member_required
def bookings_list(request):
    bookings = Booking.objects.select_related('user', 'event').order_by('-booking_date')
    return render(request, 'bookings/bookings_list.html', {'bookings': bookings})
