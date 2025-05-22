"""
Shared context processors and utilities for DJ01 project.
This module contains functions that can be used across multiple apps
to maintain consistency in templates and views.
"""

import datetime
from django.urls import reverse, NoReverseMatch

# Shared site data
SITE_INFO = {
    'app_name': 'Бронирования мероприятий',
    'current_year': datetime.datetime.now().year,
}

# Base menu structure
DEFAULT_MENU = [
    {'title': 'События', 'url_name': 'events:event_list', 'active': False, 'login_required': None},
    {'title': 'Профиль', 'url_name': 'users:profile', 'active': False, 'login_required': True},
    {'title': 'Забронировано', 'url_name': 'users:booked', 'active': False, 'login_required': True},
    {'title': 'Выход', 'url_name': 'users:logout', 'active': False, 'login_required': True},
    {'title': 'Регистрация', 'url_name': 'users:register', 'active': False, 'login_required': False},
    {'title': 'Вход', 'url_name': 'users:login', 'active': False, 'login_required': False},
    {'title': 'Контакты', 'url_name': 'contacts:contacts', 'active': False, 'login_required': None},
]

# Footer data
FOOTER_INFO = {
    'description': 'Система бронирования мероприятий',
    'links': [
        {'title': 'Политика конфиденциальности', 'url': '/privacy/'},
        {'title': 'Условия использования', 'url': '/terms/'},
        {'title': 'Карта сайта', 'url': '/sitemap/'},
    ],
    'address': 'ул. Примерная, 12, г. Москва',
    'phone': '+7987 51234567',
    'email': 'info@example.ru',
}


def get_base_context(request):
    """
    Creates a base context with common data for all pages.
    Sets the active menu item.

    Args:
        request (request): Request object

    Returns:
        dict: Context dictionary with common data
    """
    # Copy menu items to avoid modifying the original
    menu_items = DEFAULT_MENU.copy()

    # Set active menu item
    for item in menu_items:
        try:
            # Получаем URL по имени
            item['url'] = reverse(item['url_name'])
        except NoReverseMatch:
            # Если имя URL не найдено, оставляем пустой URL и логируем ошибку
            print(f"Warning: No reverse match for {item['url_name']}")
            item['url'] = '#'


        if item['url'] == '/':
            if request.path == '/':
                item['active'] = True
            else:
                item['active'] = False
        else:
            if request.path.endswith('/edit/'):
                item['active'] = request.path == item['url']
            else:
                item['active'] = ( request.path.startswith(item['url']))


    # Create base context
    context = {
        **SITE_INFO,
        'menu_items': menu_items,
        'footer': FOOTER_INFO,
        'is_authenticated': request.user.is_authenticated,
    }

    return context
