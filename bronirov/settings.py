# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@gmail.com'  # Замените на ваш email
EMAIL_HOST_PASSWORD = 'your_app_password'  # Замените на ваш пароль приложения
DEFAULT_FROM_EMAIL = 'your_email@gmail.com'  # Замените на ваш email

# Telegram settings
TELEGRAM_BOT_TOKEN = 'ваш_токен_бота'  # Замените на ваш токен бота
TELEGRAM_CHAT_ID = 'ваш_chat_id'  # Замените на ваш chat_id

# Logging settings
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'booking': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
} 