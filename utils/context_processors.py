"""
Shared context processors and utilities for DJ01 project.
This module contains functions that can be used across multiple apps
to maintain consistency in templates and views.
"""

import datetime
from django.urls import reverse, NoReverseMatch

# Shared site data
SITE_INFO = {
    'site_name': 'Бронирования мероприятий',
    'current_year': datetime.datetime.now().year,
}

# Base menu structure
DEFAULT_MENU = [
    {'title': 'Афиша событий', 'url': '/', 'active': False},
    {'title': 'Мои билеты', 'url': '/booked/', 'active': False},
    {'title': 'Профиль', 'url': '/profile/', 'active': False, 'type': 'profile'},
    {'title': 'Связаться с нами', 'url': '/contacts/', 'active': False},
]

# Footer data
FOOTER_INFO = {
    'description': 'Система бронирования мероприятий',
    'links': [
        {'title': 'Политика конфиденциальности', 'url_name': 'pages:privacy'},
        {'title': 'Условия использования', 'url_name': 'pages:terms'},
        {'title': 'Карта сайта', 'url_name': 'pages:sitemap'},
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
        if item['url'] == '/':
            if request.path == '/':
                item['active'] = True
            else:
                item['active'] = False
        else:
            if request.path.endswith('/add/'):
                item['active'] = request.path == item['url']
            else:
                item['active'] = ( request.path.startswith(item['url']))
    footer = FOOTER_INFO.copy()

    for item in footer['links']:
        try:
            item['url'] = reverse(item['url_name'])
        except NoReverseMatch:
            item['url'] = item['url_name']
        print(item)

    # Create base context
    context = {
        **SITE_INFO,
        'menu_items': menu_items,
        'footer': footer,
    }

    return context
