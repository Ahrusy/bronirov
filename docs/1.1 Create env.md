# 🔐 Настройка `.env` и подключение к `settings.py`

## 📄 1. Создание `.env` файла в корне проекта

Создайте файл `.env` рядом с `manage.py` и добавьте туда секретные и конфигурационные данные:

```env
# Django
SECRET_KEY=django-insecure-ваш-секретный-ключ
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Email
EMAIL_HOST=smtp.mail.ru
EMAIL_PORT=465
EMAIL_USE_SSL=True
EMAIL_HOST_USER=example@mail.ru
EMAIL_HOST_PASSWORD=пароль_от_почты

# Telegram
TELEGRAM_BOT_TOKEN=токен_бота
TELEGRAM_BOT_USERNAME=имя_бота
```

> ❗ Никогда не коммить `.env` в Git — добавьте его в `.gitignore`

---

## ⚙️ 2. Установка библиотеки `python-dotenv`

Добавьте в `requirements.txt`:

```txt
python-dotenv
```

или установите вручную:

```bash
pip install python-dotenv
```

---

## ⚙️ 3. Подключение `.env` в `settings.py`

В начале `settings.py` добавьте:

```python
from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')
```

---

## 🔐 4. Использование переменных в `settings.py`

### 🔑 Django:

```python
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG", "False") == "True"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")
```

### ✉️ Email:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL", "False") == "True"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
```

### 🤖 Telegram:

```python
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_BOT_USERNAME = os.getenv("TELEGRAM_BOT_USERNAME")
```

---

✅ Теперь все секреты и настройки хранятся в `.env`, а `settings.py` остаётся чистым и безопасным.
