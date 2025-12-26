"""Обработчики callback-запросов."""
import logging
from telebot import TeleBot

from utils.keyboards import get_help_keyboard
from utils.messages import HELP_MESSAGE
from utils.helpers import get_random_phrase, format_sell_prices
from utils.price_manager import price_manager
from handlers.shop import show_available_goods

logger = logging.getLogger(__name__)


def register_callback_handlers(bot: TeleBot):
    """Регистрирует обработчики callback-запросов."""
    
    @bot.callback_query_handler(func=lambda call: True)
    def callback_query(call):
        """Обработчик всех callback-запросов."""
        try:
            logger.info(f"Callback received: {call.data} from user {call.from_user.first_name}")
            req = call.data.split('_')
            command = req[0]
            
            # Создаем псевдо-message с правильным from_user
            class PseudoMessage:
                def __init__(self, original_message, real_user):
                    self.chat = original_message.chat
                    self.from_user = real_user
                    self.message_id = original_message.message_id
            
            pseudo_msg = PseudoMessage(call.message, call.from_user)
            
            if command == '/help':
                logger.info(f"Processing /help callback")
                bot.send_message(pseudo_msg.chat.id, HELP_MESSAGE)
                bot.send_message(
                    pseudo_msg.chat.id,
                    get_random_phrase(),
                    reply_markup=get_help_keyboard()
                )
                logger.info(f"/help callback completed")
            
            elif command == '/top':
                logger.info(f"Processing /top callback")
                from handlers import info as info_mod
                info_mod.top_command_impl(bot, pseudo_msg)
                logger.info(f"/top callback completed")
            
            elif command == '/cost':
                logger.info(f"Processing /cost callback")
                from handlers import shop as shop_mod
                shop_mod.cost_command_impl(bot, pseudo_msg)
                logger.info(f"/cost callback completed")
            
            elif command == '/buy':
                logger.info(f"Processing /buy callback")
                from handlers import shop as shop_mod
                shop_mod.buy_command_impl(bot, pseudo_msg)
                logger.info(f"/buy callback completed")
            
            elif command == '/myinfo':
                logger.info(f"Processing /myinfo callback")
                from handlers import info as info_mod
                info_mod.myinfo_command_impl(bot, pseudo_msg)
                logger.info(f"/myinfo callback completed")
            
            elif command == '/account':
                logger.info(f"Processing /account callback")
                from handlers import account as account_mod
                account_mod.account_command_impl(bot, pseudo_msg)
                logger.info(f"/account callback completed")
            
            elif command == '/sell':
                logger.info(f"Processing /sell callback")
                sell_prices = price_manager.get_sell_prices()
                logger.info(f"Got sell prices: {type(sell_prices)}, keys: {list(sell_prices.keys()) if isinstance(sell_prices, dict) else 'not dict'}")
                
                # Форматируем цены вручную (sell_prices это просто {animal: price})
                sell_text = "Расценки для продаж:\n\n"
                for animal, price in sell_prices.items():
                    sell_text += f"{animal}: {price} ₽\n"
                
                bot.send_message(pseudo_msg.chat.id, sell_text)
                show_available_goods(bot, pseudo_msg)
                logger.info(f"/sell callback completed")
            
        except Exception as e:
            logger.error(f"Error in callback_query: {e}")
            bot.send_message(
                call.message.chat.id,
                "Произошла ошибка. Попробуйте снова."
            )
