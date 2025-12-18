"""Обработчики информационных команд."""
import logging
from telebot import TeleBot

from utils.keyboards import get_help_keyboard
from utils.messages import HELP_MESSAGE, MYINFO_HEADER, TOP_LOOKING, TOP_FIRST
from utils.helpers import get_random_phrase, format_animals_string
from handlers.start import get_user_state

logger = logging.getLogger(__name__)


def register_info_handlers(bot: TeleBot):
    """Регистрирует обработчики информационных команд."""
    
    @bot.message_handler(func=lambda message: message.text == '/help')
    def help_command(message):
        """Показать справку."""
        try:
            bot.send_message(message.chat.id, HELP_MESSAGE)
            bot.send_message(
                message.chat.id,
                get_random_phrase(),
                reply_markup=get_help_keyboard()
            )
        except Exception as e:
            logger.error(f"Error in help_command: {e}")
    
    @bot.message_handler(func=lambda message: message.text == '/myinfo')
    def myinfo_command(message):
        """Показать информацию о пользователе."""
        us_name = message.from_user.first_name
        state = get_user_state(us_name)
        
        try:
            animals_info = format_animals_string(state.count_dict, state.add_animals)
            topplace = 3  # TODO: Реализовать подсчет места в топе
            
            display_name = state.name if state.name else us_name
            
            bot.send_message(
                message.chat.id,
                MYINFO_HEADER.format(
                    display_name,
                    state.money,
                    topplace,
                    animals_info
                )
            )
            bot.send_message(
                message.chat.id,
                get_random_phrase(),
                reply_markup=get_help_keyboard()
            )
        except Exception as e:
            logger.error(f"Error in myinfo_command: {e}")
    
    @bot.message_handler(func=lambda message: message.text == '/top')
    def top_command(message):
        """Показать топ игроков."""
        try:
            topplace = 3  # TODO: Реализовать подсчет места в топе
            
            if topplace == 1:
                message_text = TOP_LOOKING.format(TOP_FIRST)
            else:
                message_text = TOP_LOOKING.format(topplace)
            
            bot.send_message(message.chat.id, message_text)
            bot.send_message(
                message.chat.id,
                get_random_phrase(),
                reply_markup=get_help_keyboard()
            )
        except Exception as e:
            logger.error(f"Error in top_command: {e}")
