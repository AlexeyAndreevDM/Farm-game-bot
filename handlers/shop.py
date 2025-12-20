"""Обработчики магазина (покупка/продажа)."""
import logging
import datetime as dt
from telebot import TeleBot

from database.db_manager import db_manager
from config.settings import (
    ANIMALS, ANIMALS_GROW_TIME, get_animal_prices, get_sell_prices,
    ANIMAL_IMAGES, SELL_IMAGES
)
from utils.keyboards import get_animals_keyboard, get_sell_keyboard, get_help_keyboard
from utils.messages import (
    BUY_PROMPT, BUY_AMOUNT_PROMPT, BUY_SUCCESS, BUY_INVALID_AMOUNT,
    SELL_PROMPT, SELL_AMOUNT_PROMPT, SELL_PRICES_HEADER, SELL_AVAILABLE_HEADER,
    SELL_INVALID_AMOUNT, COST_MESSAGE
)
from utils.helpers import (
    get_random_phrase, validate_amount_input, 
    format_sell_prices, animals_dict_to_string
)
from handlers.start import get_user_state
from utils.price_manager import price_manager

logger = logging.getLogger(__name__)


def register_shop_handlers(bot: TeleBot):
    """Регистрирует обработчики магазина."""
    
    @bot.message_handler(func=lambda message: message.text == '/cost')
    def cost_command(message):
        """Показать цены на покупку животных."""
        try:
            animal_prices = price_manager.get_animal_prices()
            prices = list(animal_prices.values())
            bot.send_message(
                message.chat.id,
                COST_MESSAGE.format(
                    prices[0], prices[1], prices[4], 
                    prices[2], prices[3], prices[6], prices[5]
                )
            )
            bot.send_message(
                message.chat.id,
                get_random_phrase(),
                reply_markup=get_help_keyboard()
            )
        except Exception as e:
            logger.error(f"Error in cost_command: {e}")
    
    @bot.message_handler(func=lambda message: message.text == '/buy')
    def buy_command(message):
        """Команда покупки."""
        us_name = message.from_user.first_name
        state = get_user_state(us_name)
        
        try:
            state.desire = 'buy'
            bot.send_message(
                message.chat.id,
                BUY_PROMPT,
                reply_markup=get_animals_keyboard()
            )
        except Exception as e:
            logger.error(f"Error in buy_command: {e}")
    
    @bot.message_handler(func=lambda message: message.text in ANIMALS and get_user_state(message.from_user.first_name).desire == 'buy')
    def select_animal_to_buy(message):
        """Выбор животного для покупки."""
        us_name = message.from_user.first_name
        state = get_user_state(us_name)
        
        try:
            state.buyan = message.text
            
            # Отправка фото животного
            if state.buyan in ANIMAL_IMAGES:
                bot.send_photo(message.chat.id, ANIMAL_IMAGES[state.buyan])
            
            bot.send_message(message.chat.id, BUY_AMOUNT_PROMPT)
        except Exception as e:
            logger.error(f"Error in select_animal_to_buy: {e}")
    
    @bot.message_handler(func=lambda message: message.text == '/sell')
    def sell_command(message):
        """Команда продажи."""
        try:
            # Показать расценки на продажу
            sell_prices = price_manager.get_sell_prices()
            sell_prices_text = format_sell_prices(sell_prices)
            bot.send_message(
                message.chat.id,
                SELL_PRICES_HEADER.format(sell_prices_text)
            )
            
            # Показать доступные для продажи товары
            show_available_goods(bot, message)
        except Exception as e:
            logger.error(f"Error in sell_command: {e}")
    
    @bot.message_handler(func=lambda message: message.text in price_manager.get_sell_prices() and get_user_state(message.from_user.first_name).desire == 'sell')
    def select_item_to_sell(message):
        """Выбор товара для продажи."""
        us_name = message.from_user.first_name
        state = get_user_state(us_name)
        
        try:
            state.sell_it = message.text
            
            # Отправка фото
            if state.sell_it in SELL_IMAGES:
                bot.send_photo(message.chat.id, SELL_IMAGES[state.sell_it])
            
            bot.send_message(message.chat.id, SELL_AMOUNT_PROMPT)
        except Exception as e:
            logger.error(f"Error in select_item_to_sell: {e}")
    
    @bot.message_handler(func=lambda message: get_user_state(message.from_user.first_name).desire == 'buy' and message.text.isdigit())
    def process_buy(message):
        """Обработка покупки."""
        us_name = message.from_user.first_name
        state = get_user_state(us_name)
        
        try:
            animal_prices = price_manager.get_animal_prices()
            max_amount = state.money // animal_prices[state.buyan]
            is_valid, amount = validate_amount_input(message.text, max_amount)
            
            if not is_valid or amount < 1 or amount > max_amount:
                bot.send_message(message.chat.id, BUY_INVALID_AMOUNT)
                return
            
            # Покупка
            state.count_dict[state.buyan] += amount
            state.money -= animal_prices[state.buyan] * amount
            
            # Записываем статистику покупки для динамического ценообразования
            db_manager.record_purchase(state.buyan, amount)
            
            # Добавление в растущие животные
            grow_time = ANIMALS_GROW_TIME[state.buyan]
            grow_until = (dt.datetime.now() + dt.timedelta(hours=grow_time)).strftime("%A %d-%B-%y %H:%M:%S")
            state.add_animals.append([state.buyan, str(amount), grow_until])
            
            bot.send_message(
                message.chat.id,
                BUY_SUCCESS.format(state.money, grow_time)
            )
            bot.send_message(
                message.chat.id,
                get_random_phrase(),
                reply_markup=get_help_keyboard()
            )
            
            # Сохранение в БД с обновлением total_assets
            update_user_data(state)
            state.desire = ''
            
        except Exception as e:
            logger.error(f"Error in process_buy: {e}")
            bot.send_message(message.chat.id, "Ошибка при покупке. Попробуйте снова.")


def show_available_goods(bot: TeleBot, message):
    """Показать доступные для продажи товары."""
    us_name = message.from_user.first_name
    state = get_user_state(us_name)
    
    try:
        state.desire = 'sell'
        result = [SELL_AVAILABLE_HEADER]
        
        from config.settings import ANIMALS_NAMES
        
        for i, animal in enumerate(ANIMALS):
            is_growing = False
            for growing in state.add_animals:
                if animal in growing:
                    is_growing = True
                    break
            
            count = state.count_dict.get(animal, 0)
            if count != 0 and not is_growing:
                result.append(f"{ANIMALS_NAMES[i]}{count}")
        
        if len(result) > 1:
            bot.send_message(message.chat.id, '\n'.join(result))
        
        bot.send_message(
            message.chat.id,
            SELL_PROMPT,
            reply_markup=get_sell_keyboard()
        )
    except Exception as e:
        logger.error(f"Error in show_available_goods: {e}")


def update_user_data(state):
    """Обновление данных пользователя в БД."""
    try:
        animals_str = animals_dict_to_string(state.count_dict)
        
        # Подсчет total_assets
        sell_prices = price_manager.get_sell_prices()
        animals_value = 0
        for animal, count in state.count_dict.items():
            if animal in sell_prices and count > 0:
                price_dict = sell_prices[animal]
                if 1 in price_dict:
                    animals_value += price_dict[1] * count
        
        total_assets = state.money + animals_value
        
        db_manager.update_user(
            us_name=state.us_name,
            name=state.name,
            money=state.money,
            animals=animals_str,
            ad_animals='',
            total_assets=total_assets
        )
    except Exception as e:
        logger.error(f"Error updating user data: {e}")
