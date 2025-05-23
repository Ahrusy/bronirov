# bookings/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Booking
from events.models import Event
from django.contrib import messages
from .forms import BookingForm
from django.core.mail import send_mail
from django.conf import settings
import requests
from django.contrib.auth.decorators import login_required

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

@login_required
def book_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    error_message = None
    user = request.user
    profile = getattr(user, 'profile', None)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            # Проверка на дубль: один пользователь может бронировать только один раз на событие
            if Booking.objects.filter(event=event, user=user).exists():
                error_message = 'Вы уже бронировали билет на это мероприятие.'
            elif event.available_tickets < quantity:
                error_message = 'Недостаточно билетов.'
            else:
                booking = form.save(commit=False)
                booking.event = event
                booking.user = user
                booking.user_name = profile.fullname if profile else user.username
                booking.user_email = user.email
                booking.user_telegram = profile.telegram_chat_id if profile else ''
                booking.save()
                event.available_tickets -= quantity
                event.save()
                # Email уведомление
                send_mail(
                    'Подтверждение бронирования',
                    f'Здравствуйте, {booking.user_name or "гость"}! Ваше бронирование на "{event.title}" подтверждено.\nДата: {event.event_date}, Место: {event.location}, Город: {event.city}\nКоличество билетов: {booking.quantity}',
                    settings.DEFAULT_FROM_EMAIL,
                    [booking.user_email]
                )
                # Telegram уведомление админу
                admin_message = f'Новое бронирование: {booking.user_name or "гость"} на "{event.title}" ({event.event_date}), билетов: {booking.quantity}'
                send_telegram_notification(admin_message)
                # Telegram пользователю (если указан)
                if booking.user_telegram:
                    user_message = f'Ваше бронирование на "{event.title}" подтверждено! Количество билетов: {booking.quantity}'
                    send_telegram_notification(user_message, chat_id=booking.user_telegram)
                return render(request, 'booking/booking_success.html', {'event': event, 'booking': booking})
        # Если форма невалидна, ошибки будут показаны через form.errors
    else:
        form = BookingForm()
    return render(request, 'bookings/book_event.html', {'form': form, 'event': event, 'error_message': error_message})
