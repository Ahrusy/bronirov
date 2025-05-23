import os
import sys
from dotenv import load_dotenv
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode

# Автоматически загружаем переменные из .env
load_dotenv()

# Получаем токен из переменной окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_TOKEN:
    print("[ERROR] TELEGRAM_BOT_TOKEN не задан! Установите переменную окружения или создайте .env файл.\nПример: TELEGRAM_BOT_TOKEN=ваш_токен")
    sys.exit(1)

DJANGO_WEBHOOK_URL = "http://127.0.0.1:8000/bot_api/webhook/"  # ваш Django endpoint

bot = Bot(token=TELEGRAM_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

@dp.message(Command("start"))
async def handle_start(message: Message):
    # Если /start без токена — просто приветствие
    if len(message.text.split()) == 1:
        await message.answer("Привет! Для подтверждения регистрации используйте ссылку с токеном.")
        return

    # /start <токен>
    token = message.text.split(" ", 1)[1].strip()
    payload = {
        "message": {
            "text": message.text,
            "chat": {"id": message.chat.id}
        }
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(DJANGO_WEBHOOK_URL, json=payload) as resp:
            if resp.status == 200:
                data = await resp.json()
                await message.answer(data.get("reply", "✅ Telegram подтверждён!"))
            else:
                await message.answer("Ошибка подтверждения. Попробуйте позже.")

@dp.message()
async def forward_all(message: Message):
    # Пересылает все сообщения на Django endpoint (можно расширить логику)
    payload = {
        "message": {
            "text": message.text,
            "chat": {"id": message.chat.id}
        }
    }
    async with aiohttp.ClientSession() as session:
        await session.post(DJANGO_WEBHOOK_URL, json=payload)

if __name__ == "__main__":
    import asyncio
    print("[INFO] Бот запущен. Для остановки нажмите Ctrl+C.")
    asyncio.run(dp.start_polling(bot))

# ---
# Для запуска:
# 1. Создайте файл .env в корне проекта:
#    TELEGRAM_BOT_TOKEN=ваш_токен
# 2. pip install python-dotenv
# 3. Запустите: python bot_api/telegram_bot_aiogram.py
# --- 