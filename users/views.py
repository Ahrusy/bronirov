from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import ProfileForm, CustomUserCreationForm, CustomAuthenticationForm
from .models import TelegramConfirmation
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse
import qrcode
from io import BytesIO
from django.utils.crypto import get_random_string


def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = get_random_string(10)  # Генерируем уникальный username
            user.email = form.cleaned_data.get('email', '')
            user.backend = 'users.backends.EmailOrPhoneBackend'
            user.save()
            # Сохраняем профиль
            profile = user.profile
            profile.phone = form.cleaned_data.get('phone', '')
            profile.fullname = form.cleaned_data.get('fullname', '')
            profile.save()
            # Создаём токен для Telegram подтверждения
            confirmation = TelegramConfirmation.objects.create(user=user)
            login(request, user)  # автоматически залогинить
            messages.success(request, "Вы успешно зарегистрированы!")
            return redirect(reverse('users:telegram_confirm'))
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def user_profile(request):
    return render(request, 'registration/profile.html', {
        'user': request.user,
        'profile': request.user.profile
    })

@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile.fullname = form.cleaned_data.get('fullname', '')
            profile.save()
            messages.success(request, "Профиль обновлён.")
            return redirect('profile')
    else:
        initial = {
            'fullname': profile.fullname,
            'email': request.user.email,
            'phone': profile.phone,
            'telegram_chat_id': profile.telegram_chat_id,
        }
        form = ProfileForm(instance=profile, initial=initial)
    return render(request, 'registration/edit_profile.html', {'form': form})

def telegram_confirm(request):
    confirmation = None
    if request.user.is_authenticated:
        try:
            confirmation = request.user.telegram_confirmation
        except TelegramConfirmation.DoesNotExist:
            confirmation = TelegramConfirmation.objects.create(user=request.user)
    return render(request, 'registration/telegram_confirm.html', {
        'confirmation': confirmation,
        'telegram_bot_username': getattr(settings, 'TELEGRAM_BOT_USERNAME', 'your_bot_username')
    })

def telegram_qr(request):
    if not request.user.is_authenticated:
        return HttpResponse(status=403)
    try:
        confirmation = request.user.telegram_confirmation
    except TelegramConfirmation.DoesNotExist:
        return HttpResponse(status=404)
    bot_username = getattr(settings, 'TELEGRAM_BOT_USERNAME', 'your_bot_username')
    url = f"https://t.me/{bot_username}?start={confirmation.token}"
    qr = qrcode.make(url)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)
    return HttpResponse(buffer.getvalue(), content_type="image/png")

def login_user(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                return redirect(request.GET.get('next') or 'events:event_list')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})