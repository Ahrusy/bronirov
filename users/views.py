from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import ProfileForm


def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # автоматически залогинить
            messages.success(request, "Вы успешно зарегистрированы!")
            return redirect('event_list')
    else:
        form = UserCreationForm()
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
            form.save()
            messages.success(request, "Профиль обновлён.")
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'registration/edit_profile.html', {'form': form})