# bookings/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Booking
from events.models import Event
from django.contrib import messages

def book_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        booking = Booking.objects.create(
            event=event,
            user_name=request.POST.get('user_name'),
            user_email=request.POST.get('user_email'),
            user_telegram=request.POST.get('user_telegram')
        )
        messages.success(request, 'Бронирование успешно выполнено!')
        return render(request, 'bookings/booking_success.html', {
            'event': event,
            'booking': booking
        })

    return redirect('events:event_detail', pk=event_id)
