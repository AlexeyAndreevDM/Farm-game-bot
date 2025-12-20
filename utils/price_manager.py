"""Менеджер цен с автоматическим обновлением раз в сутки и динамическим ценообразованием."""
import logging
import datetime as dt
import json
import os
from typing import Dict
from random import uniform, randint

from config.settings import ANIMALS, PRICE_UPDATE_INTERVAL_HOURS

logger = logging.getLogger(__name__)

PRICES_FILE = 'prices_cache.json'

# Базовые цены для животных (минимальные)
BASE_PRICES = {
    'Корову': 10000,
    'Свинью': 5500,
    'Кролика': 350,
    'Курицу': 175,
    'Лошадь': 40000,
    'Овечку': 7250,
    'Гуся': 550
}

# Коэффициент влияния спроса на цену
DEMAND_MULTIPLIER = 0.02  # 2% прироста за каждую покупку


class PriceManager:
    """Класс для управления ценами с динамическим ценообразованием на основе спроса."""
    
    def __init__(self, db_manager):
        """Инициализация менеджера цен."""
        self.db_manager = db_manager
        self.animal_prices = {}
        self.sell_prices = {}
        self.last_update = None
        self._load_or_generate_prices()
    
    def _load_or_generate_prices(self):
        """Загрузить цены из кэша или сгенерировать новые."""
        if os.path.exists(PRICES_FILE):
            try:
                with open(PRICES_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.animal_prices = data.get('animal_prices', {})
                    self.sell_prices = data.get('sell_prices', {})
                    last_update_str = data.get('last_update')
                    
                    if last_update_str:
                        self.last_update = dt.datetime.fromisoformat(last_update_str)
                        
                        # Проверяем, нужно ли обновить цены
                        if self._should_update_prices():
                            logger.info("Prices are outdated, generating new ones based on demand")
                            self._generate_new_prices()
                        else:
                            logger.info(f"Loaded prices from cache. Next update: {self._get_next_update_time()}")
                            return
            except Exception as e:
                logger.error(f"Error loading prices from cache: {e}")
        
        # Если файла нет или произошла ошибка, генерируем новые цены
        self._generate_new_prices()
    
    def _should_update_prices(self) -> bool:
        """Проверка, нужно ли обновлять цены."""
        if not self.last_update:
            return True
        
        time_since_update = dt.datetime.now() - self.last_update
        return time_since_update.total_seconds() >= PRICE_UPDATE_INTERVAL_HOURS * 3600
    
    def _calculate_demand_price(self, animal_name: str, base_price: int, purchase_count: int) -> int:
        """Вычисляет цену на основе спроса.
        
        Формула: цена = базовая * (1 + коэффициент * количество_покупок)
        Добавляется небольшая случайность ±5% для разнообразия.
        """
        # Цена растет с каждой покупкой
        multiplier = 1 + (DEMAND_MULTIPLIER * purchase_count)
        new_price = int(base_price * multiplier)
        
        # Добавляем небольшую случайность ±5%
        variation = uniform(0.95, 1.05)
        return int(new_price * variation)
    
    def _generate_new_prices(self):
        """Генерация новых цен на основе статистики покупок."""
        # Получаем статистику покупок из базы данных
        purchase_stats = self.db_manager.get_purchase_stats()
        
        self.animal_prices = {}
        self.sell_prices = {}
        
        for animal_name in ANIMALS:
            # Получаем статистику для животного
            stats = purchase_stats.get(animal_name, {})
            purchase_count = stats.get('purchase_count', 0)
            base_price = stats.get('base_price') or BASE_PRICES.get(animal_name, 1000)
            
            # Вычисляем новую цену покупки на основе спроса
            buy_price = self._calculate_demand_price(animal_name, base_price, purchase_count)
            self.animal_prices[animal_name] = buy_price
            
            # Цена продажи = 97-99.8% от цены покупки
            sell_multiplier = uniform(0.97, 0.998)
            self.sell_prices[animal_name] = int(buy_price * sell_multiplier)
        
        self.last_update = dt.datetime.now()
        self._save_prices()
        
        # Сбрасываем счетчики покупок и обновляем базовые цены в БД
        self.db_manager.reset_purchase_stats(self.animal_prices)
        logger.info("Purchase statistics reset after price update")
        
        # Обновляем total_assets для всех игроков
        try:
            self.db_manager.update_all_total_assets(self.animal_prices, self.sell_prices)
            logger.info("Updated total_assets for all players after price change")
        except Exception as e:
            logger.error(f"Error updating total_assets: {e}")
        
        logger.info(f"Generated new demand-based prices. Next update: {self._get_next_update_time()}")
    
    def _save_prices(self):
        """Сохранение цен в кэш."""
        try:
            data = {
                'animal_prices': self.animal_prices,
                'sell_prices': self.sell_prices,
                'last_update': self.last_update.isoformat()
            }
            with open(PRICES_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info("Prices saved to cache")
        except Exception as e:
            logger.error(f"Error saving prices to cache: {e}")
    
    def _get_next_update_time(self) -> str:
        """Получение времени следующего обновления."""
        if not self.last_update:
            return "неизвестно"
        next_update = self.last_update + dt.timedelta(hours=PRICE_UPDATE_INTERVAL_HOURS)
        return next_update.strftime("%d.%m.%Y %H:%M")
    
    def get_animal_prices(self) -> Dict:
        """Получить актуальные цены на покупку животных."""
        if self._should_update_prices():
            logger.info("Auto-updating prices based on demand")
            self._generate_new_prices()
        return self.animal_prices
    
    def get_sell_prices(self) -> Dict:
        """Получить актуальные цены на продажу."""
        if self._should_update_prices():
            logger.info("Auto-updating prices based on demand")
            self._generate_new_prices()
        return self.sell_prices
    
    def force_update(self):
        """Принудительное обновление цен (для администратора)."""
        logger.info("Force updating prices based on demand")
        self._generate_new_prices()
    
    def get_time_until_update(self) -> str:
        """Получить время до следующего обновления цен."""
        if not self.last_update:
            return "неизвестно"
        
        next_update = self.last_update + dt.timedelta(hours=PRICE_UPDATE_INTERVAL_HOURS)
        time_left = next_update - dt.datetime.now()
        
        if time_left.total_seconds() <= 0:
            return "скоро"
        
        hours = int(time_left.total_seconds() // 3600)
        minutes = int((time_left.total_seconds() % 3600) // 60)
        
        return f"{hours}ч {minutes}мин"

# Глобальный экземпляр менеджера цен инициализируется в farm_game_bot.py
price_manager = None

def init_price_manager(db_manager):
    """Инициализирует глобальный экземпляр price_manager."""
    global price_manager
    price_manager = PriceManager(db_manager)
    return price_manager
