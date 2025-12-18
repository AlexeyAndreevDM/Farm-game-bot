"""Менеджер цен с автоматическим обновлением раз в сутки."""
import logging
import datetime as dt
import json
import os
from typing import Dict

from config.settings import get_animal_prices, get_sell_prices, PRICE_UPDATE_INTERVAL_HOURS

logger = logging.getLogger(__name__)

PRICES_FILE = 'prices_cache.json'


class PriceManager:
    """Класс для управления ценами с автоматическим обновлением."""
    
    def __init__(self):
        """Инициализация менеджера цен."""
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
                            logger.info("Prices are outdated, generating new ones")
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
    
    def _generate_new_prices(self):
        """Генерация новых цен."""
        self.animal_prices = get_animal_prices()
        self.sell_prices = get_sell_prices()
        self.last_update = dt.datetime.now()
        self._save_prices()
        
        # Обновляем total_assets для всех игроков
        try:
            from database.db_manager import db_manager
            db_manager.update_all_total_assets(self.animal_prices, self.sell_prices)
            logger.info("Updated total_assets for all players after price change")
        except Exception as e:
            logger.error(f"Error updating total_assets: {e}")
        
        logger.info(f"Generated new prices. Next update: {self._get_next_update_time()}")
    
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
            logger.info("Auto-updating prices")
            self._generate_new_prices()
        return self.animal_prices
    
    def get_sell_prices(self) -> Dict:
        """Получить актуальные цены на продажу."""
        if self._should_update_prices():
            logger.info("Auto-updating prices")
            self._generate_new_prices()
        return self.sell_prices
    
    def force_update(self):
        """Принудительное обновление цен (для администратора)."""
        logger.info("Force updating prices")
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


# Глобальный экземпляр менеджера цен
price_manager = PriceManager()
