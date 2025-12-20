#!/usr/bin/env python3
"""
Farm Game Bot - Телеграм бот с симулятором фермы.

Модульная архитектура с разделением на компоненты:
- config: конфигурация и константы
- database: работа с базой данных
- handlers: обработчики команд и сообщений
- utils: вспомогательные функции
"""
import logging
import sys
import telebot

from config.settings import BOT_TOKEN
from database.db_manager import db_manager
from utils.price_manager import init_price_manager

# ВАЖНО: Инициализируем price_manager ДО импорта handlers
# т.к. декораторы в handlers используют price_manager
init_price_manager(db_manager)

from handlers.start import register_start_handlers
from handlers.registration import register_registration_handlers
from handlers.shop import register_shop_handlers
from handlers.info import register_info_handlers
from handlers.callbacks import register_callback_handlers

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def main():
    """Главная функция запуска бота."""
    try:
        # Проверка наличия токена
        if not BOT_TOKEN:
            logger.error("BOT_TOKEN not found in environment variables!")
            sys.exit(1)
        
        # Инициализация бота
        bot = telebot.TeleBot(BOT_TOKEN)
        logger.info("Bot initialized successfully")
        
        # Регистрация обработчиков
        register_callback_handlers(bot)  # Должен быть первым
        register_start_handlers(bot)
        register_registration_handlers(bot)
        register_shop_handlers(bot)
        register_info_handlers(bot)
        
        logger.info("All handlers registered successfully")
        logger.info("Bot is starting...")
        
        # Запуск бота
        bot.polling(none_stop=True, interval=0)
        
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Critical error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
