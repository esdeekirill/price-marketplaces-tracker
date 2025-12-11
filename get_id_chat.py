import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not TOKEN:
    print("❌ ОШИБКА: Не найден TELEGRAM_BOT_TOKEN в .env")
    exit()

url = f"https://api.telegram.org/bot8200749853:AAHKgtj2_BZND3lScvw-anXQvoYbOJ75Q_E/getUpdates"

print("🤖 Ищу бота @EsDeePrice_Bot...")
print("📨 Напиши ему СЕЙЧАС любое сообщение в Telegram!")
print("⏳ Ожидаю 20 секунд...")

time.sleep(20)  # Ждём 20 секунд, чтобы ты успел написать

try:
    response = requests.get(url, timeout=20)
    data = response.json()

    if data.get("ok"):
        if data["result"]:
            last_msg = data["result"][-1]["message"]
            chat_id = last_msg["chat"]["id"]
            print(f"\n✅ УСПЕХ! Сообщение от @{last_msg['chat'].get('username', 'пользователя')}")
            print(f"🆔 Твой CHAT_ID: {chat_id}")
            print(f"\n📝 Добавь в файл .env строку:")
            print(f"TELEGRAM_CHAT_ID={chat_id}")
        else:
            print("\n❌ Сообщений нет. Ты точно:")
            print("   1. Нажал START в диалоге с @EsDeePrice_Bot?")
            print("   2. Написал ему сообщение после этого?")
            print("\n🔄 Попробуй ещё раз. Перезапусти скрипт и сразу напиши боту.")
    else:
        print(f"\n❌ Ошибка Telegram API: {data.get('description')}")
        print("   Проверь токен в .env")

except Exception as e:
    print(f"\n❌ Ошибка: {e}")
