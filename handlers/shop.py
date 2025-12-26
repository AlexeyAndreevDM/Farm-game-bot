"""Обработчики магазина (покупка/продажа)."""
import logging
import datetime as dt
from telebot import TeleBot

from database.db_manager import db_manager
from config.settings import (
    ANIMALS, ANIMALS_GROW_TIME, get_animal_prices, get_sell_prices,
    ANIMAL_IMAGES, SELL_IMAGES
)
from utils.keyboards import get_animals_keyboard, get_sell_keyboard, get_help_keyboard, get_back_keyboard
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


def cost_command_impl(bot: TeleBot, message):
    """Реализация показа цен на покупку (модульная функция)."""
    try:
        logger.info(f"cost_command_impl: getting prices")
        animal_prices = price_manager.get_animal_prices()
        prices = list(animal_prices.values())
        logger.info(f"cost_command_impl: got {len(prices)} prices")
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
        logger.info(f"cost_command_impl: completed")
    except Exception as e:
        logger.error(f"Error in cost_command_impl: {e}", exc_info=True)


def buy_command_impl(bot: TeleBot, message):
    """Реализация команды покупки (модульная функция)."""
    us_name = message.from_user.first_name
    state = get_user_state(us_name)
    try:
        logger.info(f"buy_command_impl: user={us_name}, setting desire='buy'")
        state.desire = 'buy'
        bot.send_message(
            message.chat.id,
            BUY_PROMPT,
            reply_markup=get_animals_keyboard()
        )
        logger.info(f"buy_command_impl: sent keyboard to user {us_name}")
    except Exception as e:
        logger.error(f"Error in buy_command_impl: {e}", exc_info=True)


def register_shop_handlers(bot: TeleBot):
    """Регистрирует обработчики магазина."""
    
    # Обработчик кнопки "Назад"
    @bot.message_handler(func=lambda message: message.text == '❌ Назад')
    def back_button(message):
        """Обработчик кнопки Назад - отмена действия."""
        us_name = message.from_user.first_name
        state = get_user_state(us_name)
        
        try:
            logger.info(f"back_button: user {us_name}, clearing desire='{state.desire}'")
            state.desire = ''
            state.buyan = ''
            state.sell_it = ''
            
            bot.send_message(
                message.chat.id,
                "↩️ Действие отменено. Возвращаемся в главное меню.",
                reply_markup=get_help_keyboard()
            )
            logger.info(f"back_button: returned to main menu")
        except Exception as e:
            logger.error(f"Error in back_button: {e}", exc_info=True)
    
    @bot.message_handler(func=lambda message: message.text == '/cost')
    def cost_command(message):
        """Показать цены на покупку животных."""
        try:
            logger.info(f"cost_command: user {message.from_user.first_name}")
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
            logger.info(f"cost_command: completed")
        except Exception as e:
            logger.error(f"Error in cost_command: {e}", exc_info=True)
    
    @bot.message_handler(func=lambda message: message.text == '/buy')
    def buy_command(message):
        """Команда покупки."""
        us_name = message.from_user.first_name
        state = get_user_state(us_name)
        
        try:
            logger.info(f"buy_command: user {us_name}, setting desire='buy', current balance={state.money}")
            state.desire = 'buy'
            
            # Показать баланс пользователя
            balance_text = f"💰 Ваш баланс: {state.money} ₽\n\n{BUY_PROMPT}"
            bot.send_message(
                message.chat.id,
                balance_text,
                reply_markup=get_animals_keyboard()
            )
            logger.info(f"buy_command: sent keyboard to {us_name}")
        except Exception as e:
            logger.error(f"Error in buy_command: {e}", exc_info=True)
    
    @bot.message_handler(func=lambda message: message.text in ANIMALS and get_user_state(message.from_user.first_name).desire == 'buy')
    def select_animal_to_buy(message):
        """Выбор животного для покупки."""
        us_name = message.from_user.first_name
        state = get_user_state(us_name)
        
        try:
            logger.info(f"select_animal_to_buy: user {us_name} selected '{message.text}', desire='{state.desire}'")
            state.buyan = message.text
            
            # Отправка фото животного
            if state.buyan in ANIMAL_IMAGES:
                bot.send_photo(message.chat.id, ANIMAL_IMAGES[state.buyan])
            
            # Показать цену и баланс
            animal_prices = price_manager.get_animal_prices()
            price = animal_prices[state.buyan]
            max_can_buy = state.money // price
            
            buy_info = f"💰 Ваш баланс: {state.money} ₽\n"
            buy_info += f"💵 Цена за {state.buyan}: {price} ₽\n"
            buy_info += f"📊 Максимум можете купить: {max_can_buy}\n\n"
            buy_info += BUY_AMOUNT_PROMPT
            
            bot.send_message(message.chat.id, buy_info, reply_markup=get_back_keyboard())
            logger.info(f"select_animal_to_buy: user {us_name} can buy max {max_can_buy}")
        except Exception as e:
            logger.error(f"Error in select_animal_to_buy: {e}", exc_info=True)
    
    @bot.message_handler(func=lambda message: message.text == '/sell')
    def sell_command(message):
        """Команда продажи."""
        us_name = message.from_user.first_name
        state = get_user_state(us_name)
        
        try:
            logger.info(f"sell_command: user {us_name}, balance={state.money}")
            
            # Показать баланс
            balance_text = f"💰 Ваш баланс: {state.money} ₽\n\n"
            
            # Показать расценки на продажу
            sell_prices = price_manager.get_sell_prices()
            logger.info(f"sell_command: got {len(sell_prices)} prices")
            
            # Форматируем цены вручную (sell_prices это {animal: price})
            sell_text = balance_text + "Расценки для продаж:\n\n"
            for animal, price in sell_prices.items():
                sell_text += f"{animal}: {price} ₽\n"
            
            bot.send_message(message.chat.id, sell_text)
            
            # Показать доступные для продажи товары
            show_available_goods(bot, message)
            logger.info(f"sell_command: completed for {us_name}")
        except Exception as e:
            logger.error(f"Error in sell_command: {e}", exc_info=True)
    
    @bot.message_handler(func=lambda message: message.text in price_manager.get_sell_prices() and get_user_state(message.from_user.first_name).desire == 'sell')
    def select_item_to_sell(message):
        """Выбор товара для продажи."""
        us_name = message.from_user.first_name
        state = get_user_state(us_name)
        
        try:
            logger.info(f"select_item_to_sell: user {us_name} selected '{message.text}', desire='{state.desire}'")
            state.sell_it = message.text
            
            # Отправка фото
            if state.sell_it in SELL_IMAGES:
                bot.send_photo(message.chat.id, SELL_IMAGES[state.sell_it])
            
            # Показать информацию о текущем количестве
            current_count = state.count_dict.get(state.sell_it, 0)
            sell_price = price_manager.get_sell_prices()[state.sell_it]
            
            sell_info = f"📦 У вас есть: {current_count} {state.sell_it}\n"
            sell_info += f"💵 Цена продажи: {sell_price} ₽\n"
            sell_info += f"💰 Текущий баланс: {state.money} ₽\n\n"
            sell_info += SELL_AMOUNT_PROMPT
            
            bot.send_message(message.chat.id, sell_info, reply_markup=get_back_keyboard())
            logger.info(f"select_item_to_sell: user {us_name} has {current_count} of {state.sell_it}")
        except Exception as e:
            logger.error(f"Error in select_item_to_sell: {e}", exc_info=True)
    
    @bot.message_handler(func=lambda message: get_user_state(message.from_user.first_name).desire == 'buy' and message.text.isdigit())
    def process_buy(message):
        """Обработка покупки."""
        us_name = message.from_user.first_name
        state = get_user_state(us_name)
        
        try:
            logger.info(f"process_buy: user {us_name} wants to buy {message.text} of {state.buyan}")
            animal_prices = price_manager.get_animal_prices()
            max_amount = state.money // animal_prices[state.buyan]
            is_valid, amount = validate_amount_input(message.text, max_amount)
            
            if not is_valid or amount < 1 or amount > max_amount:
                logger.warning(f"process_buy: invalid amount {message.text}, max={max_amount}")
                bot.send_message(message.chat.id, BUY_INVALID_AMOUNT)
                return
            
            # Покупка
            state.count_dict[state.buyan] += amount
            state.money -= animal_prices[state.buyan] * amount
            
            # Записываем статистику покупки для динамического ценообразования
            db_manager.record_purchase(state.buyan, amount)
            logger.info(f"process_buy: bought {amount}x {state.buyan}, new balance={state.money}")
            
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
            logger.info(f"process_buy: completed, desire cleared")
            
        except Exception as e:
            logger.error(f"Error in process_buy: {e}", exc_info=True)
            bot.send_message(message.chat.id, "Ошибка при покупке. Попробуйте снова.")
    
    # Отладочный обработчик для всех сообщений с животными (последний в цепочке)
    @bot.message_handler(func=lambda message: hasattr(message, 'text') and message.text in ANIMALS)
    def debug_animal_selection(message):
        """Отладочный обработчик для выбора животных."""
        us_name = message.from_user.first_name
        state = get_user_state(us_name)
        logger.warning(f"DEBUG: Animal message NOT HANDLED by specific handlers! User: {us_name}, Text: '{message.text}', Desire: '{state.desire}'")
        bot.send_message(
            message.chat.id, 
            f"⚠️ Отладка: Получено '{message.text}', но desire='{state.desire}'. Сначала нажмите /buy или /sell"
        )


def show_available_goods(bot: TeleBot, message):
    """Показать доступные для продажи товары."""
    us_name = message.from_user.first_name
    state = get_user_state(us_name)
    
    try:
        logger.info(f"show_available_goods: user {us_name}, setting desire='sell'")
        state.desire = 'sell'
        result = [SELL_AVAILABLE_HEADER]
        
        from config.settings import ANIMALS_NAMES
        
        has_animals = False
        for i, animal in enumerate(ANIMALS):
            is_growing = False
            for growing in state.add_animals:
                if animal in growing:
                    is_growing = True
                    break
            
            count = state.count_dict.get(animal, 0)
            if count != 0 and not is_growing:
                result.append(f"{ANIMALS_NAMES[i]}{count}")
                has_animals = True
        
        if has_animals:
            bot.send_message(message.chat.id, '\n'.join(result))
            bot.send_message(
                message.chat.id,
                SELL_PROMPT,
                reply_markup=get_sell_keyboard()
            )
            logger.info(f"show_available_goods: sent sell keyboard to {us_name}")
        else:
            bot.send_message(
                message.chat.id, 
                "🚫 У вас сейчас нет животных для продажи.\nКупите животных сначала через /buy",
                reply_markup=get_help_keyboard()
            )
            state.desire = ''  # Очистить desire так как продавать нечего
            logger.info(f"show_available_goods: no animals, cleared desire")
    except Exception as e:
        logger.error(f"Error in show_available_goods: {e}", exc_info=True)


def update_user_data(state):
    """Обновление данных пользователя в БД."""
    try:
        animals_str = animals_dict_to_string(state.count_dict)
        
        # Подсчет total_assets
        sell_prices = price_manager.get_sell_prices()
        animals_value = 0
        for animal, count in state.count_dict.items():
            if animal in sell_prices and count > 0:
                # sell_prices[animal] это просто число, не словарь
                animals_value += sell_prices[animal] * count
        
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
