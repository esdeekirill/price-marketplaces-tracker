# Конфигурация крипто-трекера
CRYPTO_API_URL = "https://api.coingecko.com/api/v3/simple/price"
COINS_TO_TRACK = {
    "bitcoin": {
        "symbol": "BTC", 
        "alert_price": 90000.0  # или другая цена для теста
    },
    "ethereum": {
        "symbol": "ETH", 
        "alert_price": 5000.0
    },
}
CURRENCY = "usd"
CHECK_INTERVAL_MINUTES = 5  # важно: теперь МИНУТЫ, не часы
# Конфигурация крипто-трекера
PRIMARY_API = "coingecko"  # coingecko или binance

# CoinGecko API
COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"

# Binance Public API (резервный)
BINANCE_URL = "https://api.binance.com/api/v3/ticker/price"
# Для Binance символы: BTCUSDT, ETHUSDT и т.д.

COINS_TO_TRACK = {
    "bitcoin": {
        "symbol": "BTC", 
        "alert_price": 90000.0,
        "binance_symbol": "BTCUSDT"
    },
    "ethereum": {
        "symbol": "ETH", 
        "alert_price": 5000.0,
        "binance_symbol": "ETHUSDT"
    },
}
CURRENCY = "usd"
CHECK_INTERVAL_MINUTES = 5
