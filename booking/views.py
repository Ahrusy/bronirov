# bookings/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Booking, Payment, BookingStatus
from events.models import Event
from django.contrib import messages
from .forms import BookingForm
from .notifications import send_booking_confirmation_email, send_telegram_notification
import uuid
from django.contrib.auth.decorators import login_required

@login_required
def book_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        booking = Booking.objects.create(
            event=event,
            user=request.user,
            user_name=request.POST.get('user_name'),
            user_email=request.POST.get('user_email'),
            user_telegram=request.POST.get('user_telegram'),
            status=BookingStatus.BOOKED
        )
        messages.success(request, 'Бронирование успешно выполнено!')
        return render(request, 'booking/booking_success.html', {
            'event': event,
            'booking': booking
        })

    return redirect('events:event_detail', pk=event_id)

def create_booking(request, event_id):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.event_id = event_id
            booking.save()
            
            # Отправляем уведомления
            send_booking_confirmation_email(booking)
            send_telegram_notification(booking)
            
            messages.success(request, 'Бронирование успешно создано! Проверьте вашу почту для подтверждения.')
            return redirect('event_detail', event_id=event_id)
    else:
        form = BookingForm()
    
    return render(request, 'booking/create_booking.html', {'form': form})

def process_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Создаем запись о платеже
    payment = Payment.objects.create(
        booking=booking,
        amount=booking.event.ticket_price,
        payment_id=str(uuid.uuid4()),
        payment_method='card'
    )
    
    # Имитируем успешную оплату
    payment.mark_as_completed()
    booking.status = 'CONFIRMED'
    booking.is_confirmed = True
    booking.save()
    
    # Отправляем уведомления
    send_booking_confirmation_email(booking)
    send_telegram_notification(booking)
    
    messages.success(request, 'Оплата прошла успешно! Проверьте вашу почту для подтверждения.')
    return redirect('events:event_detail', pk=booking.event.id)

@login_required
def profile(request):
    """Личный кабинет пользователя"""
    # Получаем все бронирования пользователя
    bookings = Booking.objects.filter(user=request.user).select_related('event', 'payment')
    
    context = {
        'bookings': bookings,
        'active_bookings': bookings.filter(is_confirmed=True),
        'pending_bookings': bookings.filter(is_confirmed=False),
    }
    return render(request, 'users/profile.html', context)

@login_required
def booking_detail(request, booking_id):
    """Детальная информация о бронировании"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'booking/booking_detail.html', {'booking': booking})
