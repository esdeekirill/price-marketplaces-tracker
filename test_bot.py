import os
from dotenv import load_dotenv
from telegram import Bot
from telegram.error import TelegramError

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

if not TOKEN or not CHAT_ID:
    print("❌ Ошибка: Не найден TOKEN или CHAT_ID в .env файле")
    exit()

print(f"Токен: {TOKEN[:10]}...")
print(f"Chat ID: {CHAT_ID}")

try:
    bot = Bot(token=TOKEN)
    # Пробуем отправить простое сообщение
    message = bot.send_message(
        chat_id=CHAT_ID,
        text="✅ Проверка связи! Бот жив и готов к работе!"
    )
    print("✅ Сообщение успешно отправлено!")
except TelegramError as e:
    print(f"❌ Ошибка при отправке: {e}")
