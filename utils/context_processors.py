"""
Shared context processors and utilities for DJ01 project.
This module contains functions that can be used across multiple apps
to maintain consistency in templates and views.
"""

import datetime
import logging

# Shared site data
SITE_INFO = {
    'site_name': 'Бронирования мероприятий',
    'current_year': datetime.datetime.now().year,
}

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
    # Build menu based on authentication
    menu_items = [
        {'title': 'Мероприятия', 'url': '/', 'active': False}
    ]
    
    # Check if the user attribute exists and is authenticated
    user_is_authenticated = request.user.is_authenticated if hasattr(request, 'user') else False
    
    # Add profile link only for authenticated users
    if user_is_authenticated:
        menu_items.append({'title': 'Профиль', 'url': '/profile/', 'active': False})
    else:
        # Add login and registration links for non-authenticated users
        menu_items.append({'title': 'Вход', 'url': '/users/login/', 'active': False})
        menu_items.append({'title': 'Регистрация', 'url': '/users/register/', 'active': False})

    # Set active menu item
    for item in menu_items:
        if item['url'] == '/':
            if request.path == '/':
                item['active'] = True
        else:
            item['active'] = request.path.startswith(item['url'])

    # Create base context
    context = {
        **SITE_INFO,
        'menu_items': menu_items,
        'footer': FOOTER_INFO,
    }

    return context
