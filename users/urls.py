from django.urls import path
from .views import register_user, user_profile, edit_profile,logout_user
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', logout_user, name='logout'),
    path('profile/', user_profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
]
