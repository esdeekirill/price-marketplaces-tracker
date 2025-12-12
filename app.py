from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
from datetime import datetime
import json
import subprocess
import os

app = Flask(__name__)

# Конфигурация
DB_PATH = "crypto_prices.db"

def get_db_connection():
    """Создаёт соединение с базой данных."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Для доступа к колонкам по имени
    return conn

@app.route('/')
def index():
    """Главная страница с текущими данными."""
    conn = get_db_connection()
    
    # Получаем последние цены для каждой монеты
    cursor = conn.cursor()
    cursor.execute('''
        SELECT coin_symbol, price_usd, timestamp 
        FROM price_history 
        WHERE id IN (
            SELECT MAX(id) 
            FROM price_history 
            GROUP BY coin_symbol
        )
        ORDER BY coin_symbol
    ''')
    latest_prices = cursor.fetchall()
    
    # Получаем последние 20 записей для таблицы истории
    cursor.execute('''
        SELECT coin_symbol, price_usd, timestamp 
        FROM price_history 
        ORDER BY timestamp DESC 
        LIMIT 20
    ''')
    history = cursor.fetchall()
    
    conn.close()
    
    return render_template('index.html', 
                          latest_prices=latest_prices, 
                          history=history)

@app.route('/api/prices')
def api_prices():
    """JSON API для получения текущих цен (может пригодиться для JS)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT coin_symbol, price_usd, timestamp 
        FROM price_history 
        WHERE id IN (
            SELECT MAX(id) 
            FROM price_history 
            GROUP BY coin_symbol
        )
    ''')
    
    prices = []
    for row in cursor.fetchall():
        prices.append({
            'coin': row['coin_symbol'],
            'price': row['price_usd'],
            'time': row['timestamp']
        })
    
    conn.close()
    return jsonify(prices)

@app.route('/chart/<coin_symbol>')
def generate_chart(coin_symbol):
    """Генерирует и показывает график для указанной монеты."""
    # Вызываем наш скрипт visualize.py для конкретной монеты
    try:
        # Импортируем функцию из visualize.py
        from visualize import plot_price_history
        chart_path = plot_price_history(coin_symbol, hours=24)
        
        if chart_path and os.path.exists(chart_path):
            # Простой способ - перенаправляем на файл
            return redirect(f'/{chart_path}')
        else:
            return f"Не удалось построить график для {coin_symbol}", 500
    except Exception as e:
        return f"Ошибка: {str(e)}", 500

@app.route('/add_coin', methods=['POST'])
def add_coin():
    """Добавляет новую монету для отслеживания (упрощённо)."""
    # В реальном приложении здесь была бы логика добавления в config.py
    # Сейчас просто покажем сообщение
    coin_name = request.form.get('coin_name', '').strip()
    coin_symbol = request.form.get('coin_symbol', '').strip().upper()
    
    if coin_name and coin_symbol:
        # Здесь можно добавить логику сохранения в config.py
        return f"Монета {coin_symbol} ({coin_name}) добавлена в список отслеживания! (функция в разработке)"
    else:
        return "Ошибка: заполните все поля", 400

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 Запуск Flask веб-интерфейса для Crypto Tracker")
    print("🌐 Откройте в браузере: http://localhost:5079")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5079)
