import requests
import time
import schedule
from datetime import datetime
from config import TEST_API_URL, CHECK_INTERVAL_HOURS
from utils.notifier import send_notification  # <-- Импорт для Telegram

def fetch_data(api_url):
    """Функция для получения данных по API."""
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()  # Проверяем, не была ли ошибка HTTP
        data = response.json()
        print(f"[{datetime.now()}] Данные успешно получены.")
        return data
    except requests.exceptions.RequestException as e:
        print(f"[{datetime.now()}] Ошибка при запросе к API: {e}")
        return None

def job():
    """Основная задача, которая выполняется по расписанию."""
    print(f"[{datetime.now()}] Запуск проверки...")
    data = fetch_data(TEST_API_URL)

    if data:
        # Выводим полученные данные в консоль
        print(f"Получены данные: {data}")

        # Отправляем уведомление в Telegram
        notification_msg = (
            f"✅ Проверка #{datetime.now().strftime('%H:%M')}\n"
            f"Данные получены. Заголовок: {data.get('title', 'Без заголовка')[:50]}..."
        )
        send_notification(notification_msg)  # <-- Отправка в Telegram
    else:
        print("Данные не получены, пропускаем итерацию.")

def main():
    """Основная функция, настраивающая и запускающую планировщик."""
    print("Запуск Price Tracker...")
    # Запускаем задачу сразу при старте
    job()

    # Настраиваем периодический запуск (например, раз в 24 часа)
    schedule.every(CHECK_INTERVAL_HOURS).hours.do(job)

    # Бесконечный цикл для работы планировщика
    while True:
        schedule.run_pending()
        time.sleep(60)  # Проверяем каждую минуту

if __name__ == "__main__":
    main()
