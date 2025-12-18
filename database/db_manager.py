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
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS goods (
                        us_name TEXT PRIMARY KEY,
                        name TEXT NOT NULL,
                        money INTEGER NOT NULL,
                        animals TEXT NOT NULL,
                        ad_animals TEXT NOT NULL
                    )
                ''')
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
                   animals: str = '', ad_animals: str = ''):
        """Создание нового пользователя."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT INTO goods (us_name, name, money, animals, ad_animals) VALUES (?, ?, ?, ?, ?)',
                    (us_name, name, money, animals, ad_animals)
                )
                logger.info(f"User {us_name} created successfully")
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            raise
    
    def update_user(self, us_name: str, name: str, money: int, 
                   animals: str, ad_animals: str):
        """Обновление данных пользователя."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
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
        """Получение топа пользователей по деньгам."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                result = cursor.execute(
                    'SELECT name, money FROM goods ORDER BY money DESC LIMIT ?',
                    (limit,)
                ).fetchall()
                return result
        except Exception as e:
            logger.error(f"Error getting top users: {e}")
            return []


# Глобальный экземпляр менеджера БД
db_manager = DatabaseManager()
