import asyncio
from datetime import datetime
import pytz
from telethon import TelegramClient, events

# 🔐 Данные
API_ID = 21018756
API_HASH = '5fce0349ea49d2c1717d197f8536d1b5'
SESSION_NAME = 'countdown_session'
PHONE_NUMBER = '+88805727142'

# 🎯 Целевое время
TARGET_TIME = datetime(2025, 6, 10, 9, 0, 0, tzinfo=pytz.timezone('Europe/Moscow'))

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# Функция отсчёта
def get_time_remaining():
    now = datetime.now(pytz.timezone('Europe/Moscow'))
    diff = TARGET_TIME - now
    if diff.total_seconds() <= 0:
        return None
    total_seconds = int(diff.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"До 10 июня 09:00 (МСК) осталось:\n" \
           f"⏳ {hours:02}:{minutes:02}:{seconds:02}"

# Команда /отсчет
@client.on(events.NewMessage(pattern='/отсчет'))
async def handler(event):
    msg_text = get_time_remaining()
    if not msg_text:
        await event.reply("⏰ Время уже наступило!")
        return
    message = await event.respond(msg_text)
    while True:
        await asyncio.sleep(60)
        msg_text = get_time_remaining()
        if not msg_text:
            await message.edit("⏰ Время наступило!")
            break
        try:
            await message.edit(msg_text)
        except Exception as e:
            print(f"Ошибка при обновлении сообщения: {e}")
            break

# Команда /люблюсоню
@client.on(events.NewMessage(pattern='/люблюсоню'))
async def love_sonya(event):
    await event.reply("мяУ МЯУ (meow gav gav )")

# Запуск
async def main():
    print("🔑 Подключение к Telegram...")
    await client.start(PHONE_NUMBER)
    print("✅ Бот работает. Ждёт команды /отсчет или /люблюсоню")
    await client.run_until_disconnected()

if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())
