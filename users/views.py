from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import ProfileForm
from booking.models import Booking, BookingStatus
from .models import Notification


def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # автоматически залогинить
            messages.success(request, "Вы успешно зарегистрированы!")
            return redirect('events:event_list')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def logout_user(request):
    """Выход пользователя из системы"""
    if request.method == 'POST':
        logout(request)
        messages.success(request, "Вы успешно вышли из системы")
    return redirect('events:event_list')

@login_required
def user_profile(request):
    return render(request, 'users/profile.html', {
        'user': request.user,
        'profile': request.user.profile
    })

@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль обновлён.")
            return redirect('users:profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'users/edit_profile.html', {'form': form})

@login_required
def profile(request):
    """Личный кабинет пользователя"""
    active_bookings = Booking.objects.filter(user=request.user, status=BookingStatus.CONFIRMED)
    pending_bookings = Booking.objects.filter(user=request.user, status=BookingStatus.BOOKED)
    history_bookings = Booking.objects.filter(user=request.user).exclude(status__in=[BookingStatus.CONFIRMED, BookingStatus.BOOKED])
    return render(request, 'users/profile.html', {
        'active_bookings': active_bookings,
        'pending_bookings': pending_bookings,
        'history_bookings': history_bookings
    })

@login_required
def booking_detail(request, booking_id):
    """Детальная информация о бронировании"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'users/booking_detail.html', {'booking': booking})

def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.status = 'cancelled'
    booking.save()
    Notification.objects.create(user=request.user, message=f"Бронирование '{booking.event.title}' было отменено.")
    return redirect('users:profile')