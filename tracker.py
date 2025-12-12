import requests
import time
import schedule
from datetime import datetime
from config import CRYPTO_API_URL, COINS_TO_TRACK, CURRENCY, CHECK_INTERVAL_MINUTES
from utils.notifier import send_notification

def get_crypto_price(coin_id="bitcoin"):
    """
    Получает текущую цену криптовалюты с CoinGecko API.
    
    Args:
        coin_id (str): ID монеты на CoinGecko (например, 'bitcoin', 'ethereum')
    
    Returns:
        float: Текущая цена или None в случае ошибки
    """
    try:
        params = {
            "ids": coin_id,
            "vs_currencies": CURRENCY
        }
        
        response = requests.get(CRYPTO_API_URL, params=params, timeout=10)
        response.raise_for_status()  # Проверяем на HTTP-ошибки
        data = response.json()
        
        price = data[coin_id][CURRENCY]
        print(f"[{datetime.now()}] Цена {coin_id.upper()}: ${price:,.2f}")
        return price
        
    except requests.exceptions.RequestException as e:
        print(f"[{datetime.now()}] Ошибка сети при запросе цены {coin_id}: {e}")
    except KeyError as e:
        print(f"[{datetime.now()}] Ошибка в структуре данных API для {coin_id}: {e}")
    except Exception as e:
        print(f"[{datetime.now()}] Неожиданная ошибка при получении цены {coin_id}: {e}")
    
    return None

def check_and_notify(coin_id, coin_config):
    """
    Проверяет цену конкретной монеты и отправляет уведомление при достижении цели.
    """
    symbol = coin_config["symbol"]
    alert_price = coin_config["alert_price"]
    
    current_price = get_crypto_price(coin_id)
    if current_price is None:
        return  # Прерываем, если не получили цену
    
    # Проверяем, достигнута ли целевая цена
    if current_price >= alert_price:
        price_diff = current_price - alert_price
        message = (
            f"🚨 **АЛЕРТ: {symbol} достиг ${current_price:,.2f}**\n"
            f"Целевая цена: ${alert_price:,.0f}\n"
            f"Превышение: +${price_diff:,.2f}\n"
            f"Время: {datetime.now().strftime('%H:%M:%S')}"
        )
        send_notification(message)
        print(f"[{datetime.now()}] Уведомление отправлено для {symbol}!")
    else:
        # Логируем для отладки
        remaining = alert_price - current_price
        print(f"[{datetime.now()}] {symbol}: ${current_price:,.2f} (до цели: ${remaining:,.2f})")

def job():
    """Основная задача, которая запускается по расписанию."""
    print(f"\n[{datetime.now()}] ===== ПРОВЕРКА КРИПТО-РЫНКА =====")
    
    # Проверяем все монеты из конфига
    for coin_id, coin_config in COINS_TO_TRACK.items():
        check_and_notify(coin_id, coin_config)
        time.sleep(1)  # Небольшая задержка между запросами к API

def main():
    """Основная функция, запускающая планировщик."""
    print("=" * 50)
    print("🚀 ЗАПУСК КРИПТО-ТРЕКЕРА")
    print(f"📊 Отслеживаем: {', '.join([c['symbol'] for c in COINS_TO_TRACK.values()])}")
    print(f"⏰ Интервал проверки: каждые {CHECK_INTERVAL_MINUTES} минут")
    print("=" * 50)
    
    # Первый запуск сразу
    job()
    
    # Настраиваем периодический запуск
    schedule.every(CHECK_INTERVAL_MINUTES).minutes.do(job)
    
    # Бесконечный цикл для планировщика
    print(f"\n[{datetime.now()}] Трекер запущен. Ожидаю уведомлений...")
    print("Для остановки нажмите Ctrl+C\n")
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # Проверяем каждую минуту

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n[{datetime.now()}] Трекер остановлен пользователем.")
