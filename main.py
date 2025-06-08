import threading
from flask import Flask
from telethon import TelegramClient, events
import pytz
import datetime
import asyncio

# Flask-сервер для предотвращения сна Replit
app = Flask(__name__)

@app.route('/')
def home():
    return "Бот работает!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

threading.Thread(target=run_flask).start()

# Настройки Telegram
api_id = 21018756
api_hash = "5fce0349ea49d2c1717d197f8536d1b5"
session_name = "countdown_session"  # .session файл должен быть в папке

# Создание клиента
client = TelegramClient(session_name, api_id, api_hash)

# Цель — 10 июня 9:00 по МСК
target_time = datetime.datetime(2025, 6, 10, 9, 0, 0, tzinfo=pytz.timezone('Europe/Moscow'))

@client.on(events.NewMessage(pattern='/отсчет'))
async def countdown_handler(event):
    msg = await event.respond("⏳ Считаем...")

    while True:
        now = datetime.datetime.now(pytz.timezone('Europe/Moscow'))
        diff = target_time - now

        if diff.total_seconds() <= 0:
            await msg.edit("✅ Время пришло!")
            break

        days, remainder = divmod(int(diff.total_seconds()), 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, _ = divmod(remainder, 60)

        countdown = f"⏳ До 10 июня 9:00 (МСК): {days}д {hours}ч {minutes}м"
        try:
            await msg.edit(countdown)
        except:
            pass

        await asyncio.sleep(60)

@client.on(events.NewMessage(pattern='/люблюсоню'))
async def love_handler(event):
    await event.respond("❤️гав гав")

# Запуск клиента
print("🔑 Подключение к Telegram...")
client.start()
print("✅ Бот работает. Ждёт команду /отсчет или /люблюсоню")

client.run_until_disconnected()
