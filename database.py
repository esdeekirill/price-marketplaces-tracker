import sqlite3
from datetime import datetime
import os

DB_PATH = "crypto_prices.db"

def init_db():
    """Инициализирует базу данных и создаёт таблицу, если её нет."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            coin_symbol TEXT NOT NULL,
            price_usd REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Создаём индекс для быстрого поиска по монете и времени
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_coin_time 
        ON price_history (coin_symbol, timestamp)
    ''')
    
    conn.commit()
    conn.close()
    print(f"[{datetime.now()}] База данных инициализирована: {DB_PATH}")

def save_price(coin_symbol, price_usd):
    """Сохраняет цену монеты в базу данных."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO price_history (coin_symbol, price_usd)
        VALUES (?, ?)
    ''', (coin_symbol, price_usd))
    
    conn.commit()
    conn.close()
    return cursor.lastrowid

def get_price_history(coin_symbol, hours=24):
    """
    Возвращает историю цен для указанной монеты за последние N часов.
    
    Returns:
        list of tuples: [(timestamp, price), ...]
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT timestamp, price_usd 
        FROM price_history 
        WHERE coin_symbol = ? 
        AND timestamp >= datetime('now', ?)
        ORDER BY timestamp
    ''', (coin_symbol, f'-{hours} hours'))
    
    data = cursor.fetchall()
    conn.close()
    return data

def get_price_stats(coin_symbol, hours=24):
    """
    Возвращает статистику по цене монеты за период.
    
    Returns:
        dict: {'min': , 'max': , 'avg': , 'change': , 'volatility': }
    """
    history = get_price_history(coin_symbol, hours)
    if not history:
        return None
    
    prices = [price for _, price in history]
    
    return {
        'min': min(prices),
        'max': max(prices),
        'avg': sum(prices) / len(prices),
        'change': ((prices[-1] - prices[0]) / prices[0] * 100) if prices[0] != 0 else 0,
        'samples': len(prices)
    }

# При импорте автоматически инициализируем БД
if not os.path.exists(DB_PATH):
    init_db()
def ensure_db_initialized():
    """Гарантирует, что база данных и таблицы созданы."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Проверяем, существует ли таблица
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='price_history'
    """)
    
    if not cursor.fetchone():
        print(f"[{datetime.now()}] Таблица не найдена, создаём...")
        init_db()
    else:
        print(f"[{datetime.now()}] База данных уже инициализирована")
    
    conn.close()

# Гарантируем инициализацию при импорте модуля
ensure_db_initialized()
