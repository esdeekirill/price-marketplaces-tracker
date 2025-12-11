import os
import asyncio
from dotenv import load_dotenv
from telegram import Bot
from telegram.error import TelegramError

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

async def send_notification_async(message):
    """Асинхронная функция для отправки уведомления в Telegram."""
    if not TOKEN or not CHAT_ID:
        print("[ОШИБКА] Не настроен токен бота или CHAT_ID.")
        return False
    
    try:
        bot = Bot(token=TOKEN)
        await bot.send_message(chat_id=CHAT_ID, text=message)
        print(f"[УВЕДОМЛЕНИЕ ОТПРАВЛЕНО] {message}")
        return True
    except TelegramError as e:
        print(f"[ОШИБКА ТЕЛЕГРАМ] Не удалось отправить сообщение: {e}")
        return False

def send_notification(message):
    """Синхронная обёртка для асинхронной функции отправки."""
    try:
        # Запускаем асинхронную функцию в событийном цикле
        return asyncio.run(send_notification_async(message))
    except RuntimeError:
        # Если цикл уже запущен (например, в асинхронном приложении)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(send_notification_async(message))
        loop.close()
        return result
