"""Обработчики информационных команд."""
import logging
from telebot import TeleBot

from utils.keyboards import get_help_keyboard
from utils.messages import HELP_MESSAGE, MYINFO_HEADER, TOP_LOOKING, TOP_FIRST
from utils.helpers import get_random_phrase, format_animals_string
from handlers.start import get_user_state
from database.db_manager import db_manager

logger = logging.getLogger(__name__)


def myinfo_command_impl(bot: TeleBot, message):
    """Реализация показа информации о пользователе (модульная функция)."""
    us_name = message.from_user.first_name
    state = get_user_state(us_name)
    try:
        animals_info = format_animals_string(state.count_dict, state.add_animals)
        topplace = db_manager.get_user_rank(us_name)
        if topplace == 0:
            topplace = "-"
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
        logger.error(f"Error in myinfo_command_impl: {e}")


def top_command_impl(bot: TeleBot, message):
    """Реализация показа топа игроков (модульная функция)."""
    try:
        us_name = message.from_user.first_name
        topplace = db_manager.get_user_rank(us_name)
        top_users = db_manager.get_top_users(10)
        if topplace == 1:
            user_place_text = TOP_LOOKING.format(TOP_FIRST)
        elif topplace > 0:
            user_place_text = TOP_LOOKING.format(topplace)
        else:
            user_place_text = "Так, посмотрим...\nВы еще не зарегистрированы в игре."
        bot.send_message(message.chat.id, user_place_text)
        if top_users:
            top_text = "\n🏆 ТОП-10 ФЕРМЕРОВ:\n\n"
            medals = ["🥇", "🥈", "🥉"]
            for idx, (name, assets) in enumerate(top_users, 1):
                medal = medals[idx - 1] if idx <= 3 else f"{idx}."
                top_text += f"{medal} {name} - {assets:,} ₽\n"
            bot.send_message(message.chat.id, top_text)
        bot.send_message(
            message.chat.id,
            get_random_phrase(),
            reply_markup=get_help_keyboard()
        )
    except Exception as e:
        logger.error(f"Error in top_command_impl: {e}")


def register_info_handlers(bot: TeleBot):
    """Регистрирует обработчики информационных команд."""
    
    @bot.message_handler(func=lambda message: message.text == '/help')
    def help_command(message):
        """Показать справку."""
        try:
            logger.info(f"help_command: user {message.from_user.first_name}")
            bot.send_message(message.chat.id, HELP_MESSAGE)
            bot.send_message(
                message.chat.id,
                get_random_phrase(),
                reply_markup=get_help_keyboard()
            )
            logger.info(f"help_command: completed")
        except Exception as e:
            logger.error(f"Error in help_command: {e}", exc_info=True)
    
    @bot.message_handler(func=lambda message: message.text == '/myinfo')
    def myinfo_command(message):
        """Показать информацию о пользователе."""
        us_name = message.from_user.first_name
        state = get_user_state(us_name)
        
        try:
            logger.info(f"myinfo_command: user {us_name}")
            animals_info = format_animals_string(state.count_dict, state.add_animals)
            
            # Получаем реальное место в топе
            topplace = db_manager.get_user_rank(us_name)
            if topplace == 0:
                topplace = "-"
            
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
            logger.info(f"myinfo_command: completed, rank={topplace}")
        except Exception as e:
            logger.error(f"Error in myinfo_command: {e}", exc_info=True)
    
    @bot.message_handler(func=lambda message: message.text == '/top')
    def top_command(message):
        """Показать топ игроков."""
        try:
            logger.info(f"top_command: user {message.from_user.first_name}")
            us_name = message.from_user.first_name
            
            # Получаем место пользователя
            topplace = db_manager.get_user_rank(us_name)
            
            # Получаем топ-10 игроков
            top_users = db_manager.get_top_users(10)
            logger.info(f"top_command: user rank={topplace}, top_users count={len(top_users)}")
            
            # Формируем сообщение
            if topplace == 1:
                user_place_text = TOP_LOOKING.format(TOP_FIRST)
            elif topplace > 0:
                user_place_text = TOP_LOOKING.format(topplace)
            else:
                user_place_text = "Так, посмотрим...\nВы еще не зарегистрированы в игре."
            
            bot.send_message(message.chat.id, user_place_text)
            
            # Показываем топ-10
            if top_users:
                top_text = "\n🏆 ТОП-10 ФЕРМЕРОВ:\n\n"
                medals = ["🥇", "🥈", "🥉"]
                
                for idx, (name, assets) in enumerate(top_users, 1):
                    medal = medals[idx - 1] if idx <= 3 else f"{idx}."
                    top_text += f"{medal} {name} - {assets:,} ₽\n"
                
                bot.send_message(message.chat.id, top_text)
            
            bot.send_message(
                message.chat.id,
                get_random_phrase(),
                reply_markup=get_help_keyboard()
            )
            logger.info(f"top_command: completed")
        except Exception as e:
            logger.error(f"Error in top_command: {e}", exc_info=True)
