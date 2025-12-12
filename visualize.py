import matplotlib.pyplot as plt
from database import get_price_history
from datetime import datetime
import os

def plot_price_history(coin_symbol="BTC", hours=24, save_path="charts"):
    """
    Строит график изменения цены и сохраняет его как изображение.
    """
    # Получаем данные
    history = get_price_history(coin_symbol, hours)
    if not history:
        print(f"Нет данных для {coin_symbol} за последние {hours} часов")
        return None
    
    # Подготавливаем данные
    timestamps = [datetime.fromisoformat(ts.replace('Z', '+00:00')) for ts, _ in history]
    prices = [price for _, price in history]
    
    # Создаём график
    plt.figure(figsize=(12, 6))
    plt.plot(timestamps, prices, marker='o', linewidth=2, markersize=4)
    
    # Настройки графика
    plt.title(f'История цены {coin_symbol} за последние {hours} часов', fontsize=14, pad=20)
    plt.xlabel('Время')
    plt.ylabel(f'Цена (USD)')
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Создаём папку для графиков
    os.makedirs(save_path, exist_ok=True)
    
    # Сохраняем график
    filename = f"{save_path}/{coin_symbol}_{datetime.now().strftime('%Y%m%d_%H%M')}.png"
    plt.savefig(filename, dpi=100)
    plt.close()
    
    print(f"График сохранён: {filename}")
    return filename

if __name__ == "__main__":
    # Пример использования
    plot_price_history("BTC", hours=24)
    plot_price_history("ETH", hours=12)
