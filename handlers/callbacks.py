"""Обработчики callback-запросов."""
import logging
from telebot import TeleBot

from utils.keyboards import get_help_keyboard
from utils.messages import HELP_MESSAGE
from utils.helpers import get_random_phrase, format_sell_prices
from config.settings import get_sell_prices
from handlers.shop import show_available_goods, sell_prices

logger = logging.getLogger(__name__)


def register_callback_handlers(bot: TeleBot):
    """Регистрирует обработчики callback-запросов."""
    
    @bot.callback_query_handler(func=lambda call: True)
    def callback_query(call):
        """Обработчик всех callback-запросов."""
        try:
            req = call.data.split('_')
            command = req[0]
            
            if command == '/help':
                bot.send_message(call.message.chat.id, HELP_MESSAGE)
                bot.send_message(
                    call.message.chat.id,
                    get_random_phrase(),
                    reply_markup=get_help_keyboard()
                )
            
            elif command == '/top':
                from handlers.info import top_command
                top_command(call.message)
            
            elif command == '/cost':
                from handlers.shop import cost_command
                cost_command(call.message)
            
            elif command == '/buy':
                from handlers.shop import buy_command
                buy_command(call.message)
            
            elif command == '/myinfo':
                from handlers.info import myinfo_command
                myinfo_command(call.message)
            
            elif command == '/sell':
                sell_prices_text = format_sell_prices(sell_prices)
                bot.send_message(
                    call.message.chat.id,
                    f'Вот расценки для продаж:\n\n{sell_prices_text}'
                )
                show_available_goods(bot, call.message)
            
        except Exception as e:
            logger.error(f"Error in callback_query: {e}")
            bot.send_message(
                call.message.chat.id,
                "Произошла ошибка. Попробуйте снова."
            )
