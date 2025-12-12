# Конфигурация крипто-трекера
CRYPTO_API_URL = "https://api.coingecko.com/api/v3/simple/price"
COINS_TO_TRACK = {
    "bitcoin": {
        "symbol": "BTC", 
        "alert_price": 90000.0  # USD
    },
    "ethereum": {
        "symbol": "ETH", 
        "alert_price": 5000.0  # USD
    },
}
CURRENCY = "usd"
CHECK_INTERVAL_MINUTES = 5  # Проверяем каждые 5 минут (не часов!)
