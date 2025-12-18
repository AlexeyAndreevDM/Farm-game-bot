"""Обработчики регистрации."""
import logging
from telebot import TeleBot

from database.db_manager import db_manager
from config.settings import INITIAL_MONEY
from utils.keyboards import get_registration_keyboard, get_confirmation_keyboard, get_help_keyboard
from utils.messages import REG_PROMPT, REG_ALREADY, REG_CONFIRM, REG_INVALID, REG_SUCCESS
from utils.helpers import get_random_phrase, animals_dict_to_string
from handlers.start import get_user_state

logger = logging.getLogger(__name__)


def register_registration_handlers(bot: TeleBot):
    """Регистрирует обработчики регистрации."""
    
    @bot.message_handler(func=lambda message: message.text == '/reg')
    def registration_command(message):
        """Обработчик команды /reg."""
        us_name = message.from_user.first_name
        state = get_user_state(us_name)
        
        try:
            if state.name == '':
                bot.send_message(
                    message.chat.id,
                    REG_PROMPT,
                    reply_markup=get_registration_keyboard()
                )
            else:
                bot.send_message(
                    message.from_user.id,
                    REG_ALREADY.format(state.name)
                )
        except Exception as e:
            logger.error(f"Error in registration_command: {e}")
    
    @bot.message_handler(func=lambda message: message.text == 'Буду использовать свой стандартный ник')
    def use_default_name(message):
        """Использование стандартного ника."""
        us_name = message.from_user.first_name
        state = get_user_state(us_name)
        
        try:
            state.name = us_name
            save_user_account(state)
            
            bot.send_message(message.chat.id, REG_SUCCESS)
            bot.send_message(
                message.chat.id,
                get_random_phrase(),
                reply_markup=get_help_keyboard()
            )
        except Exception as e:
            logger.error(f"Error in use_default_name: {e}")
            bot.send_message(message.chat.id, "Ошибка при сохранении. Попробуйте снова.")
    
    @bot.message_handler(func=lambda message: message.text == 'Введу свой ник')
    def enter_custom_name(message):
        """Ввод своего ника."""
        bot.register_next_step_handler(message, get_name)
    
    @bot.message_handler(func=lambda message: message.text == 'Да, ник - супер!')
    def confirm_name(message):
        """Подтверждение ника."""
        us_name = message.from_user.first_name
        state = get_user_state(us_name)
        
        try:
            save_user_account(state)
            
            bot.send_message(message.chat.id, REG_SUCCESS)
            bot.send_message(
                message.chat.id,
                get_random_phrase(),
                reply_markup=get_help_keyboard()
            )
        except Exception as e:
            logger.error(f"Error in confirm_name: {e}")
            bot.send_message(message.chat.id, "Ошибка при сохранении. Попробуйте снова.")
    
    @bot.message_handler(func=lambda message: message.text == 'Нет, надо по-другому')
    def reject_name(message):
        """Отклонение ника."""
        bot.send_message(message.chat.id, REG_INVALID)
        bot.register_next_step_handler(message, get_name)
    
    def get_name(message):
        """Получение имени пользователя."""
        us_name = message.from_user.first_name
        state = get_user_state(us_name)
        
        state.name = message.text
        bot.send_message(
            message.chat.id,
            REG_CONFIRM.format(message.text),
            reply_markup=get_confirmation_keyboard()
        )
    
    def save_user_account(state: 'UserState'):
        """Сохранение аккаунта пользователя."""
        animals_str = animals_dict_to_string(state.count_dict)
        
        if not db_manager.user_exists(state.us_name):
            db_manager.create_user(
                us_name=state.us_name,
                name=state.name,
                money=INITIAL_MONEY,
                animals=animals_str,
                ad_animals='',
                total_assets=INITIAL_MONEY
            )
            state.money = INITIAL_MONEY
            logger.info(f"Created new user: {state.us_name}")
