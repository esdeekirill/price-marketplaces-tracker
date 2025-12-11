import requests
import time
import schedule
from datetime import datetime
from config import TEST_API_URL, CHECK_INTERVAL_HOURS

def fetch_data(api_url):
    """Функция для получения данных по API."""
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()  # Проверяем, не была ли ошибка HTTP
        data = response.json()
        print(f"[{datetime.now()}] Данные успешно получены.")
        # Здесь будет логика извлечения конкретной цены
        return data
    except requests.exceptions.RequestException as e:
        print(f"[{datetime.now()}] Ошибка при запросе к API: {e}")
        return None

def job():
    """Основная задача, которая выполняется по расписанию."""
    print(f"[{datetime.now()}] Запуск проверки...")
    data = fetch_data(TEST_API_URL)

    if data:
        # Временная заглушка: просто выводим полученные данные
        print(f"Получены данные: {data}")
        # В будущем здесь будет вызов функции для отправки уведомления
        # и сохранения данных в БД для сравнения
    else:
        print("Данные не получены, пропускаем итерацию.")

def main():
    """Основная функция, настраивающая и запускающая планировщик."""
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
