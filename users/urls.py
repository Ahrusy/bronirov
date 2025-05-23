from django.urls import path
from .views import register_user, user_profile, edit_profile, telegram_confirm, telegram_qr, login_user
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page=reverse_lazy('events:event_list')), name='logout'),
    path('profile/', user_profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('telegram-confirm/', telegram_confirm, name='telegram_confirm'),
    path('telegram-qr/', telegram_qr, name='telegram_qr'),
]
