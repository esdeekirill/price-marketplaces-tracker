from config import COINGECKO_URL, BINANCE_URL, COINS_TO_TRACK, CURRENCY, CHECK_INTERVAL_MINUTES
import requests
import time
import schedule
from datetime import datetime
from config import CRYPTO_API_URL, COINS_TO_TRACK, CURRENCY, CHECK_INTERVAL_MINUTES
from utils.notifier import send_notification
from database import save_price, get_price_stats

def get_crypto_price(coin_id="bitcoin"):
    """
    Получает текущую цену криптовалюты, используя основной или резервный API.
    """
    coin_config = COINS_TO_TRACK.get(coin_id, {})
    symbol = coin_config.get("symbol", coin_id.upper())
    
    # Пробуем CoinGecko (основной API)
    try:
        params = {"ids": coin_id, "vs_currencies": CURRENCY}
        response = requests.get(COINGECKO_URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if coin_id in data:
            price = data[coin_id][CURRENCY]
            print(f"[{datetime.now()}] ✅ CoinGecko: {symbol} = ${price:,.2f}")
            return price
    except Exception as e:
        print(f"[{datetime.now()}] ⚠️ CoinGecko недоступен: {e}")
    
    # Если CoinGecko не сработал, пробуем Binance (резервный API)
    try:
        binance_symbol = coin_config.get("binance_symbol", f"{symbol}USDT")
        response = requests.get(f"{BINANCE_URL}?symbol={binance_symbol}", timeout=5)
        response.raise_for_status()
        data = response.json()
        
        price = float(data["price"])
        print(f"[{datetime.now()}] 🔄 Binance: {symbol} = ${price:,.2f}")
        return price
    except Exception as e:
        print(f"[{datetime.now()}] ❌ Оба API недоступны для {symbol}: {e}")
    
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
    
    # Сохраняем цену в базу данных
    save_price(symbol, current_price)
    
    # Получаем статистику за последние 24 часа
    stats = get_price_stats(symbol, hours=24)
    if stats:
        print(f"[{datetime.now()}] Статистика {symbol}: "
              f"мин ${stats['min']:,.2f}, макс ${stats['max']:,.2f}, "
              f"изменение {stats['change']:+.2f}%")
    
    # Проверяем, достигнута ли целевая цена
    if current_price >= alert_price:
        price_diff = current_price - alert_price
        
        # Создаём сообщение со статистикой
        message = (
            f"🚨 **АЛЕРТ: {symbol} достиг ${current_price:,.2f}**\n"
            f"Целевая цена: ${alert_price:,.0f}\n"
            f"Превышение: +${price_diff:,.2f}\n"
        )
        
        if stats:
            message += (
                f"📊 За 24ч: мин ${stats['min']:,.2f}, макс ${stats['max']:,.2f}\n"
                f"📈 Изменение: {stats['change']:+.2f}%\n"
            )
        
        message += f"🕐 Время: {datetime.now().strftime('%H:%M:%S')}"
        
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
    print("🚀 ЗАПУСК КРИПТО-ТРЕКЕРА С БАЗОЙ ДАННЫХ")
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
