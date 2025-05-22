from datetime import datetime

def common_context(request):
    return {
        'site_name': 'Бронирование мероприятий',
        'current_year': datetime.now().year,
        'menu_items': [
            {'title': 'Главная', 'url': '/', 'active': request.path == '/'},
            {'title': 'Мероприятия', 'url': '/', 'active': request.path == '/'},
            {'title': 'Личный кабинет', 'url': '/profile/', 'active': request.path.startswith('/profile/')},
        ],
        'footer': {
            'description': 'Сервис для бронирования мероприятий',
            'links': [
                {'title': 'О нас', 'url': '#'},
                {'title': 'Контакты', 'url': '#'},
                {'title': 'Правила', 'url': '#'},
            ],
            'address': 'г. Москва, ул. Примерная, д. 1',
            'phone': '+7 (999) 123-45-67',
            'email': 'info@example.com',
        }
    } 