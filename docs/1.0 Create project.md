# 🛠️ Подготовка Django-проекта и структуры приложений

## 📦 Установка Django

```bash
# Установить Django 4.2 (в активированном окружении)
pip install django==4.2
```

## 📄 Создание файла зависимостей

```bash
# Создать requirements.txt с текущими установленными пакетами
pip freeze > requirements.txt
```

> 💡 Или заранее создать `requirements.txt` вручную с содержимым:
> ```
> django==4.2
> ```

---

## 📁 1. Создание проекта Django

```bash
django-admin startproject event_booking .
```

> ⚠️ Точка (`.`) обязательна для создания проекта в текущем каталоге (в корне проекта).

---

## 📦 2. Создание приложений

```bash
python manage.py startapp users
python manage.py startapp events
python manage.py startapp booking
python manage.py startapp bot_api
python manage.py startapp event_importer
```

---

## 📂 3. Создание общей папки для шаблонов

```bash
mkdir templates
```

---

## 📂 4. Создание подпапок шаблонов для каждого приложения

```bash
mkdir templates\users
mkdir templates\events
mkdir templates\booking
mkdir templates\bot_api
mkdir templates\event_importer
mkdir templates\registration  # для встроенных форм login/logout
```

---

✅ После этого можно настроить `TEMPLATES` в `settings.py`:

```python
TEMPLATES = [
    {
        ...
        'DIRS': [BASE_DIR / 'templates'],
        ...
    },
]
```

## 🚀 Первый запуск проекта

```bash
# 1. Применить миграции
python manage.py makemigrations
python manage.py migrate

# 2. Создать суперпользователя
python manage.py createsuperuser

# 3. Запустить сервер
python manage.py runserver
```

Перейдите в браузере по адресу:

```
http://127.0.0.1:8000
```

И войдите в административную панель:

```
http://127.0.0.1:8000/admin/
```

Теперь вы готовы к разработке!
