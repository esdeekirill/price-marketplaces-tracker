import os
import asyncio
import sys
from dotenv import load_dotenv
from telegram import Bot
from telegram.error import TelegramError

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

print("=" * 50)
print("🔧 ТЕСТ ОТПРАВКИ СООБЩЕНИЯ В TELEGRAM (Async Fix)")
print("=" * 50)
print(f"Токен (первые 10 символов): {TOKEN[:10] if TOKEN else 'НЕ НАЙДЕН'}")
print(f"Chat ID из .env: {CHAT_ID or 'НЕ НАЙДЕН'}")

if not TOKEN or not CHAT_ID:
    print("❌ ОШИБКА: Проверь, что в файле .env есть TOKEN и CHAT_ID")
    sys.exit(1)

async def main():
    try:
        bot = Bot(token=TOKEN)
        print("✅ Бот инициализирован")
        
        # Пробуем отправить тестовое сообщение
        test_msg = "🛠️ ТЕСТ: Сообщение от бота через async/await! Если ты это видишь, всё настроено верно!"
        print(f"📤 Отправляю сообщение: '{test_msg}'")
        
        sent_message = await bot.send_message(chat_id=CHAT_ID, text=test_msg)
        print("✅ Сообщение отправлено успешно!")
        print(f"   ID сообщения: {sent_message.message_id}")
        return True
        
    except TelegramError as e:
        print(f"❌ Ошибка Telegram: {e}")
        print("\n🔍 Возможные причины и решения:")
        print("1. Бот заблокирован - разблокируй @EsDeePrice_Bot в Telegram")
        print("2. Неверный Chat ID - получи его через @userinfobot")
        print("3. Проблемы с интернет-соединением")
        return False
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")
        return False

# Запускаем асинхронную функцию
if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
