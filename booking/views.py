# bookings/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Booking
from events.models import Event
from django.contrib import messages
from .forms import BookingForm
from django.core.mail import send_mail
from django.conf import settings
import requests

def send_telegram_notification(message, chat_id=None):
    token = settings.TELEGRAM_BOT_TOKEN
    if not chat_id:
        chat_id = getattr(settings, 'TELEGRAM_CHAT_ID', None)
    if not token or not chat_id:
        return
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    data = {'chat_id': chat_id, 'text': message}
    try:
        requests.post(url, data=data, timeout=5)
    except Exception:
        pass

def book_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    error_message = None
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['user_email']
            # Проверка на дубль
            if Booking.objects.filter(event=event, user_email=user_email).exists():
                error_message = 'Вы уже бронировали билет на это мероприятие.'
            elif event.available_tickets < 1:
                error_message = 'Билеты закончились.'
            else:
                booking = form.save(commit=False)
                booking.event = event
                booking.save()
                event.available_tickets -= 1
                event.save()
                # Email уведомление
                send_mail(
                    'Подтверждение бронирования',
                    f'Здравствуйте, {booking.user_name or "гость"}! Ваше бронирование на "{event.title}" подтверждено.\nДата: {event.event_date}, Место: {event.location}, Город: {event.city}',
                    settings.DEFAULT_FROM_EMAIL,
                    [booking.user_email]
                )
                # Telegram уведомление админу
                admin_message = f'Новое бронирование: {booking.user_name or "гость"} на "{event.title}" ({event.event_date})'
                send_telegram_notification(admin_message)
                # Telegram пользователю (если указан)
                if booking.user_telegram:
                    user_message = f'Ваше бронирование на "{event.title}" подтверждено!'
                    send_telegram_notification(user_message, chat_id=booking.user_telegram)
                return render(request, 'booking/booking_success.html', {'event': event, 'booking': booking})
        # Если форма невалидна, ошибки будут показаны через form.errors
    else:
        form = BookingForm()
    return render(request, 'bookings/book_event.html', {'form': form, 'event': event, 'error_message': error_message})
