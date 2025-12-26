"""Модели данных для работы с базой данных."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Farmer:
    """Модель фермера."""
    us_name: str  # Telegram username
    name: str  # Никнейм в игре
    money: int  # Деньги
    animals: str  # Животные (строка с количествами через пробел)
    ad_animals: str  # Растущие животные


@dataclass
class UserState:
    """Состояние пользователя в боте."""
    us_name: str
    name: str = ''
    money: int = 50000  # Начальный баланс 50000
    desire: str = ''  # 'buy' или 'sell'
    buyan: str = ''  # Животное для покупки
    sell_it: str = ''  # Животное/продукт для продажи
    count_dict: dict = None  # Словарь с количеством животных
    products: dict = None  # Словарь с продуктами
    add_animals: list = None  # Список растущих животных
    
    def __post_init__(self):
        """Инициализация дефолтных значений."""
        if self.count_dict is None:
            self.count_dict = {
                'Корову': 0, 'Свинью': 0, 'Кролика': 0, 
                'Курицу': 0, 'Лошадь': 0, 'Овечку': 0, 'Гуся': 0
            }
        if self.products is None:
            self.products = {
                'Коровье молоко': 0, 
                'Куриные яйца': 0, 
                'Овечью шерсть': 0
            }
        if self.add_animals is None:
            self.add_animals = []
