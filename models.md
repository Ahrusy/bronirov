
## 🧩 **Основные сущности (модели)**

Мы моделируем 2 ключевых объекта:

```
🗓️ Event — мероприятие
👤 Booking — бронирование мероприятия
```

---

### 🧱 1. Модель `Event` — 🗓️ Мероприятие

```python
class Event(models.Model):
    title = models.CharField(max_length=200)  # Название мероприятия
    description = models.TextField(blank=True)  # Описание
    event_date = models.DateField()  # Дата проведения
    start_time = models.TimeField(blank=True, null=True)  # Время начала (опц.)
    location = models.CharField(max_length=200)  # Адрес / место
    city = models.CharField(max_length=100, blank=True, null=True)  # Город
    genre = models.CharField(max_length=100)  # Тип события (концерт, выставка...)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена
    available_tickets = models.PositiveIntegerField(default=100)  # Остаток билетов
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)  # Афиша
    rules = models.TextField(blank=True, null=True)  # Правила посещения
    event_url = models.URLField(blank=True, null=True)  # Внешняя ссылка
    source = models.CharField(max_length=50, blank=True, null=True)  # Источник данных
```

#### 🔍 Пояснение:

| Поле                | Назначение                                               |
| ------------------- | -------------------------------------------------------- |
| `title`             | отображается в списке и в карточках                      |
| `description`       | дополнительная информация для пользователей              |
| `event_date`        | ключевая для сортировки и фильтра                        |
| `start_time`        | уточнение по времени, опционально                        |
| `location/city`     | помогают в фильтрации и поиске                           |
| `genre`             | позволяет фильтровать по типу                            |
| `ticket_price`      | может быть 0 (бесплатное событие) или платное            |
| `available_tickets` | нужно для ограничения бронирований                       |
| `image`             | используется на карточке и странице мероприятия          |
| `rules`             | тексты "вход с паспортом", "маски обязательны" и т.п.    |
| `event_url`         | если пользователь хочет перейти на источник              |
| `source`            | указывает откуда загружено (например, manual/import/API) |

---

### 🧾 2. Модель `Booking` — 👤 Бронирование

```python
class Booking(models.Model):
    user_name = models.CharField(max_length=100)  # Имя
    user_email = models.EmailField()  # Email
    user_telegram = models.CharField(max_length=100, blank=True, null=True)  # @username (опц.)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bookings')  # связка
    booking_date = models.DateField(auto_now_add=True)  # Дата бронирования
```

#### 🔍 Пояснение:

| Поле            | Назначение                                                          |
| --------------- | ------------------------------------------------------------------- |
| `user_name`     | отображается в админке и в уведомлениях                             |
| `user_email`    | используется для отправки email-подтверждений                       |
| `user_telegram` | используется для уведомлений в Telegram                             |
| `event` (FK)    | связь N:1 с `Event` — пользователь бронирует конкретное мероприятие |
| `booking_date`  | автоматически фиксируется, для аналитики и отображения              |

📌 Django `on_delete=models.CASCADE` гарантирует, что при удалении мероприятия — связанные брони удаляются автоматически (логично).

---

## 🔗 Связи между таблицами

```txt
Event (1) <——— (N) Booking
```

* Одно мероприятие может иметь много бронирований.
* Одно бронирование связано только с одним мероприятием.

---

## 🛡️ Бизнес-правила (в коде, но связаны с БД)

* ❗ У одного пользователя (по email) не может быть 2 бронирования одного и того же события
* ❗ Кол-во билетов не может уйти в минус
* ✅ После бронирования: `available_tickets -= 1`, создаётся запись Booking

---

## 🧠 Возможное расширение

Позже можно добавить:

| Возможность               | Что нужно                                     |
| ------------------------- | --------------------------------------------- |
| Авторизация пользователей | `User` model + `ForeignKey` в `Booking`       |
| Онлайн-оплата             | `Order`, `Payment` таблицы                    |
| Расписание и спикеры      | `Session`, `Speaker`, `Tag` модели            |
| Локации как сущности      | `Location` модель с отдельным адресом и залом |

