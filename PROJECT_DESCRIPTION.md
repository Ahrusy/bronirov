# Бронирование мероприятий

## Командная разработка

### Цели проекта
1. Упростить процесс бронирования мероприятий для пользователей
2. Автоматизировать управление билетами и уведомлениями
3. Обеспечить безопасность и масштабируемость

## Стек технологий
- Python, Django, Django ORM
- Django Templates, Bootstrap 5, HTML5, CSS3, JavaScript
- SQLite (dev), PostgreSQL (prod)
- Telegram Bot (aiogram), QR-коды (qrcode)
- Docker (опционально), Gunicorn, Nginx, Git
- Django TestCase, pytest (опционально)

## Основные технические требования
- Регистрация и аутентификация пользователей (с подтверждением через Telegram)
- Регистрация: только ФИО, email, телефон, пароль. Username не запрашивается, генерируется автоматически.
- Вход по email или телефону и паролю (username не используется).
- Просмотр, фильтрация и бронирование событий
- Личный кабинет пользователя с историей бронирований
- Интеграция с Telegram-ботом для подтверждения и уведомлений
- Генерация QR-кодов для подтверждения Telegram
- Адаптивный дизайн
- Админ-панель
- Безопасный выход (logout через POST)
- Логирование и обработка ошибок
- Бронирование только для авторизованных пользователей
- В бронировании указывается количество билетов, остальные данные подтягиваются из профиля
- Уникальность бронирования по (user, event)
- В профиле и везде отображается ФИО (profile.fullname), если оно заполнено
- Email не уникален, но при входе используется первый найденный

## Команда и задачи
- Backend: бизнес-логика, интеграции, база данных
- Frontend: шаблоны, UI/UX, адаптивность
- DevOps: деплой, безопасность
- Тестировщик: тестирование
- Project Manager: задачи, сроки, коммуникация

## Этапы разработки
### Этап 1: Проектирование и базовая архитектура
Описание: Анализ требований, проектирование моделей, настройка Django, регистрация, вход, структура событий.

### Этап 2: Интеграция Telegram и расширение функционала
Описание: Подтверждение через Telegram, QR-коды, интеграция с ботом, уведомления.

### Этап 3: UI/UX, тестирование, деплой
Описание: Улучшение интерфейса, тестирование, деплой, безопасность.

## Метрики проекта
- Количество пользователей
- Подтвержденные Telegram-аккаунты
- Успешные бронирования
- Среднее время отклика

## Техническая реализация
- Django-приложения: users, events, booking, bot_api
- Модели: User, Event, Booking, TelegramConfirmation
- Вьюхи: регистрация (с ФИО, email, телефоном), вход (по email/телефону и паролю), подтверждение Telegram, бронирование (только для авторизованных, с количеством билетов), личный кабинет
- Интеграция с Telegram через aiogram-бота
- Генерация QR-кодов
- Уникальность бронирования по (user, event)
- В "Мои билеты" отображаются все данные: ФИО, email, Telegram, название события, дата, количество билетов, дата бронирования
- В профиле отображается ФИО, если оно заполнено

## Архитектура проекта
- Модульная структура Django
- Использование namespace для url
- Разделение backend и frontend
- Внешние интеграции в отдельных приложениях
- Безопасность: CSRF, logout через POST, токены в .env
- Кнопки "Войти" и "Регистрация" только в выпадающем меню профиля

## Полученные выводы
1. Интеграция с Telegram повышает вовлечённость и безопасность
2. Namespace в url предотвращает ошибки маршрутизации
3. Современный UI/UX критичен для опыта пользователя
4. Уникальность бронирования и автоматизация профиля повышают удобство и защищённость
5. ФИО пользователя теперь отображается в профиле и везде, где требуется идентификация

## Демонстрация проекта
- Запуск: `python manage.py runserver`
- Telegram-бот: .env с TELEGRAM_BOT_TOKEN, запуск `python bot_api/telegram_bot_aiogram.py`
- Тестирование: http://127.0.0.1:8000/ 