"""Менеджер базы данных."""
import sqlite3
import logging
from typing import Optional, Tuple
from contextlib import contextmanager

from config.settings import DB_NAME, INITIAL_MONEY

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Класс для работы с базой данных SQLite."""
    
    def __init__(self, db_name: str = DB_NAME):
        """Инициализация менеджера БД."""
        self.db_name = db_name
        self._init_database()
    
    @contextmanager
    def _get_connection(self):
        """Контекстный менеджер для работы с соединением БД."""
        conn = sqlite3.connect(self.db_name)
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            conn.close()
    
    def _init_database(self):
        """Инициализация таблиц в базе данных."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                # Создание таблицы
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS goods (
                        us_name TEXT PRIMARY KEY,
                        name TEXT NOT NULL,
                        money INTEGER NOT NULL,
                        animals TEXT NOT NULL,
                        ad_animals TEXT NOT NULL,
                        total_assets INTEGER DEFAULT 0
                    )
                ''')
                
                # Миграция: добавление поля total_assets если его нет
                cursor.execute("PRAGMA table_info(goods)")
                columns = [column[1] for column in cursor.fetchall()]
                if 'total_assets' not in columns:
                    cursor.execute('ALTER TABLE goods ADD COLUMN total_assets INTEGER DEFAULT 0')
                    logger.info("Added total_assets column to database")
                
                logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
    
    def user_exists(self, us_name: str) -> bool:
        """Проверка существования пользователя."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                result = cursor.execute(
                    'SELECT us_name FROM goods WHERE us_name = ?',
                    (us_name,)
                ).fetchone()
                return result is not None
        except Exception as e:
            logger.error(f"Error checking user existence: {e}")
            return False
    
    def get_user_name(self, us_name: str) -> Optional[str]:
        """Получение имени пользователя."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                result = cursor.execute(
                    'SELECT name FROM goods WHERE us_name = ?',
                    (us_name,)
                ).fetchone()
                return result[0].strip() if result else None
        except Exception as e:
            logger.error(f"Error getting user name: {e}")
            return None
    
    def get_user_data(self, us_name: str) -> Optional[Tuple]:
        """Получение всех данных пользователя."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                result = cursor.execute(
                    'SELECT * FROM goods WHERE us_name = ?',
                    (us_name,)
                ).fetchone()
                return result
        except Exception as e:
            logger.error(f"Error getting user data: {e}")
            return None
    
    def create_user(self, us_name: str, name: str, money: int = INITIAL_MONEY, 
                   animals: str = '', ad_animals: str = '', total_assets: int = None):
        """Создание нового пользователя."""
        try:
            if total_assets is None:
                total_assets = money
            
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT INTO goods (us_name, name, money, animals, ad_animals, total_assets) VALUES (?, ?, ?, ?, ?, ?)',
                    (us_name, name, money, animals, ad_animals, total_assets)
                )
                logger.info(f"User {us_name} created successfully")
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            raise
    
    def update_user(self, us_name: str, name: str, money: int, 
                   animals: str, ad_animals: str, total_assets: int = None):
        """Обновление данных пользователя."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                if total_assets is not None:
                    cursor.execute(
                        '''UPDATE goods 
                           SET name = ?, money = ?, animals = ?, ad_animals = ?, total_assets = ? 
                           WHERE us_name = ?''',
                        (name, money, animals, ad_animals, total_assets, us_name)
                    )
                else:
                    cursor.execute(
                        '''UPDATE goods 
                           SET name = ?, money = ?, animals = ?, ad_animals = ? 
                           WHERE us_name = ?''',
                        (name, money, animals, ad_animals, us_name)
                    )
                logger.info(f"User {us_name} updated successfully")
        except Exception as e:
            logger.error(f"Error updating user: {e}")
            raise
    
    def get_top_users(self, limit: int = 10) -> list:
        """Получение топа пользователей по суммарной стоимости активов."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                result = cursor.execute(
                    'SELECT name, total_assets FROM goods ORDER BY total_assets DESC LIMIT ?',
                    (limit,)
                ).fetchall()
                return result
        except Exception as e:
            logger.error(f"Error getting top users: {e}")
            return []
    
    def get_user_rank(self, us_name: str) -> int:
        """Получение места пользователя в рейтинге."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                # Получаем все данные пользователя
                user_data = cursor.execute(
                    'SELECT total_assets FROM goods WHERE us_name = ?',
                    (us_name,)
                ).fetchone()
                
                if not user_data:
                    return 0
                
                user_assets = user_data[0]
                
                # Считаем сколько игроков имеют больше активов
                rank = cursor.execute(
                    'SELECT COUNT(*) + 1 FROM goods WHERE total_assets > ?',
                    (user_assets,)
                ).fetchone()[0]
                
                return rank
        except Exception as e:
            logger.error(f"Error getting user rank: {e}")
            return 0
    
    def update_all_total_assets(self, animal_prices: dict, sell_prices: dict):
        """Обновление total_assets для всех пользователей при изменении цен."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                users = cursor.execute('SELECT us_name, money, animals FROM goods').fetchall()
                
                from utils.helpers import string_to_animals_dict
                
                for us_name, money, animals_str in users:
                    animals_dict = string_to_animals_dict(animals_str)
                    
                    # Подсчет стоимости животных
                    animals_value = 0
                    for animal, count in animals_dict.items():
                        if animal in sell_prices and count > 0:
                            # Используем цену продажи для 1 животного
                            price_dict = sell_prices[animal]
                            if 1 in price_dict:
                                animals_value += price_dict[1] * count
                    
                    total_assets = money + animals_value
                    
                    cursor.execute(
                        'UPDATE goods SET total_assets = ? WHERE us_name = ?',
                        (total_assets, us_name)
                    )
                
                logger.info("Updated total_assets for all users")
        except Exception as e:
            logger.error(f"Error updating all total_assets: {e}")


# Глобальный экземпляр менеджера БД
db_manager = DatabaseManager()
