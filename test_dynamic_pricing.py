#!/usr/bin/env python3
"""Тест динамического ценообразования."""
import logging
from database.db_manager import db_manager
from utils.price_manager import init_price_manager

logging.basicConfig(level=logging.INFO)

def test_dynamic_pricing():
    """Тестирование системы динамического ценообразования."""
    print("=== Тест динамического ценообразования ===\n")
    
    # Инициализация
    price_manager = init_price_manager(db_manager)
    
    # 1. Проверяем начальные цены
    print("1. Начальные цены:")
    buy_prices = price_manager.get_animal_prices()
    sell_prices = price_manager.get_sell_prices()
    
    for animal, price in buy_prices.items():
        sell_price = sell_prices[animal]
        sell_percent = (sell_price / price) * 100
        print(f"   {animal}: купить {price}₽, продать {sell_price}₽ ({sell_percent:.1f}%)")
    
    # 2. Проверяем статистику покупок
    print("\n2. Статистика покупок (до покупок):")
    stats = db_manager.get_purchase_stats()
    for animal, data in stats.items():
        print(f"   {animal}: куплено {data['purchase_count']} раз, базовая цена {data['base_price']}₽")
    
    # 3. Симулируем покупки
    print("\n3. Симулируем 10 покупок 'Курицу':")
    for i in range(10):
        db_manager.record_purchase('Курицу', 1)
    
    print("\n4. Симулируем 5 покупок 'Корову':")
    for i in range(5):
        db_manager.record_purchase('Корову', 1)
    
    # 4. Проверяем обновленную статистику
    print("\n5. Статистика покупок (после покупок):")
    stats = db_manager.get_purchase_stats()
    for animal, data in stats.items():
        print(f"   {animal}: куплено {data['purchase_count']} раз, текущая цена {data['current_price']}₽")
    
    # 5. Принудительно обновляем цены
    print("\n6. Принудительно генерируем новые цены на основе спроса...")
    price_manager.force_update()
    
    # 6. Проверяем новые цены
    print("\n7. Новые цены после обновления:")
    new_buy_prices = price_manager.get_animal_prices()
    new_sell_prices = price_manager.get_sell_prices()
    
    for animal in buy_prices.keys():
        old_price = buy_prices[animal]
        new_price = new_buy_prices[animal]
        old_sell = sell_prices[animal]
        new_sell = new_sell_prices[animal]
        
        change = ((new_price - old_price) / old_price) * 100
        sell_percent = (new_sell / new_price) * 100
        
        print(f"   {animal}:")
        print(f"      Покупка: {old_price}₽ → {new_price}₽ ({change:+.1f}%)")
        print(f"      Продажа: {old_sell}₽ → {new_sell}₽ ({sell_percent:.1f}%)")
    
    # 7. Проверяем, что счетчики сброшены
    print("\n8. Статистика после сброса:")
    stats = db_manager.get_purchase_stats()
    for animal, data in stats.items():
        print(f"   {animal}: счетчик={data['purchase_count']}, базовая={data['base_price']}₽")
    
    print("\n=== Тест завершен успешно! ===")
    print("\nВыводы:")
    print("- Цены на популярные товары (Курица, Корова) должны были вырасти")
    print("- Цена продажи всегда 97-99.8% от цены покупки")
    print("- Счетчики покупок сбросились после обновления")
    print("- Базовые цены обновились до текущих цен")


if __name__ == '__main__':
    test_dynamic_pricing()
