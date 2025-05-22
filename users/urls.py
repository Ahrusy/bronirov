from django.urls import path
from .views import register_user, user_profile, edit_profile, logout_user
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', logout_user, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('booking/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('cancel_booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]
