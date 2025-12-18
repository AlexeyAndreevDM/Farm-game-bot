"""Обработчик команды /start."""
import logging
from telebot import TeleBot

from database.db_manager import db_manager
from database.models import UserState
from utils.keyboards import get_help_keyboard
from utils.messages import WELCOME_MESSAGE_NEW, WELCOME_MESSAGE_EXISTING
from utils.helpers import get_random_phrase, string_to_animals_dict

logger = logging.getLogger(__name__)

# Хранилище состояний пользователей
user_states = {}


def get_user_state(us_name: str) -> UserState:
    """Получает или создает состояние пользователя."""
    if us_name not in user_states:
        user_states[us_name] = UserState(us_name=us_name)
    return user_states[us_name]


def register_start_handlers(bot: TeleBot):
    """Регистрирует обработчики для команды /start."""
    
    @bot.message_handler(commands=['start'])
    def start_message(message):
        """Обработчик команды /start."""
        us_name = message.from_user.first_name
        state = get_user_state(us_name)
        
        try:
            # Проверяем существование пользователя
            if db_manager.user_exists(us_name):
                name = db_manager.get_user_name(us_name)
                
                if name and name != '':
                    # Загружаем данные пользователя
                    user_data = db_manager.get_user_data(us_name)
                    if user_data:
                        state.name = user_data[1]
                        state.money = user_data[2]
                        state.count_dict = string_to_animals_dict(user_data[3])
                        # ad_animals = user_data[4]
                    
                    bot.send_message(
                        message.chat.id,
                        WELCOME_MESSAGE_EXISTING.format(name)
                    )
                    bot.send_message(
                        message.chat.id,
                        get_random_phrase(),
                        reply_markup=get_help_keyboard()
                    )
                    return
            
            # Новый пользователь
            bot.send_message(
                message.chat.id,
                WELCOME_MESSAGE_NEW.format(us_name)
            )
            bot.send_message(
                message.chat.id,
                get_random_phrase(),
                reply_markup=get_help_keyboard()
            )
            
        except Exception as e:
            logger.error(f"Error in start_message: {e}")
            bot.send_message(
                message.chat.id,
                "Произошла ошибка. Попробуйте позже."
            )
