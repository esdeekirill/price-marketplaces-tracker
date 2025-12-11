import os
import time
from dotenv import load_dotenv
import requests

# Загружаем токен из .env файла
load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not TOKEN:
    print("❌ ОШИБКА: Не найден TELEGRAM_BOT_TOKEN в файле .env")
    print("Убедись, что файл .env существует и содержит строку: TELEGRAM_BOT_TOKEN=твой_токен")
    exit()

# URL API Telegram для получения обновлений
url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"

print("🔄 Запрашиваю обновления у Telegram...")
print("📨 Пожалуйста, напиши ЛЮБОЕ сообщение своему боту в Telegram прямо сейчас!")
print("⏳ Ожидаю 10 секунд...")

# Даём время отправить сообщение
time.sleep(10)

try:
    response = requests.get(url, timeout=15)
    data = response.json()

    if data["ok"] and data["result"]:
        # Берём последнее сообщение из списка обновлений
        last_update = data["result"][-1]
        chat_id = last_update["message"]["chat"]["id"]
        
        print("✅ УСПЕХ!")
        print(f"📋 Твой CHAT_ID: {chat_id}")
        print("\n📝 Добавь эту строчку в файл .env:")
        print(f"TELEGRAM_CHAT_ID={chat_id}")
    else:
        print("❌ Сообщений не обнаружено.")
        print("Убедись, что:")
        print("1. Ты написал сообщение боту (@my_price_tracker_bot)")
        print("2. Бот активирован (ты нажал START в диалоге с ним)")
        print("3. Токен в файле .env указан верно")

except Exception as e:
    print(f"❌ Ошибка при запросе: {e}")
