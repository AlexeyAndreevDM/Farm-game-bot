"""Обработчик управления аккаунтами."""
import logging
from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from database.db_manager import db_manager
from handlers.start import get_user_state, user_states
from utils.keyboards import get_help_keyboard
from utils.helpers import get_random_phrase

logger = logging.getLogger(__name__)


def account_command_impl(bot: TeleBot, message):
    """Реализация команды управления аккаунтом (модульная функция)."""
    telegram_user = message.from_user.first_name
    telegram_id = message.from_user.id
    
    try:
        logger.info(f"account_command_impl: telegram_user={telegram_user}, telegram_id={telegram_id}")
        
        # Проверяем текущий аккаунт пользователя
        current_state = get_user_state(telegram_user)
        
        # Проверяем что пользователь существует И что у него есть name (аккаунт создан)
        if db_manager.user_exists(telegram_user) and current_state.name != '':
            # Пользователь уже зарегистрирован и аккаунт создан
            user_data = db_manager.get_user_data(telegram_user)
            name = user_data[1] if user_data else telegram_user
            money = user_data[2] if user_data else 0
            
            account_info = f"👤 **Информация об аккаунте:**\n\n"
            account_info += f"🆔 Telegram: {telegram_user}\n"
            account_info += f"🎮 Ваш никнейм: {name}\n"
            account_info += f"💰 Баланс: {money} ₽\n\n"
            account_info += f"Выберите действие:"
            
            # Клавиатура с опциями управления аккаунтом
            markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup.add(KeyboardButton('✏️ Сменить ник'))
            markup.add(KeyboardButton('🗑 Удалить аккаунт'))
            markup.add(KeyboardButton('❌ Отмена'))
            
            bot.send_message(message.chat.id, account_info, reply_markup=markup, parse_mode='Markdown')
        else:
            # Новый пользователь или аккаунт не создан
            account_info = f"👋 Добро пожаловать в Ферма Бот, {telegram_user}!\n\n"
            account_info += f"У вас еще нет игрового аккаунта.\n"
            account_info += f"Создать аккаунт с начальным балансом 50000 ₽?"
            
            markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup.add(KeyboardButton('✅ Создать аккаунт'))
            markup.add(KeyboardButton('❌ Отмена'))
            
            bot.send_message(message.chat.id, account_info, reply_markup=markup)
        
        logger.info(f"account_command_impl: sent account info")
    except Exception as e:
        logger.error(f"Error in account_command_impl: {e}", exc_info=True)
        bot.send_message(message.chat.id, "Ошибка при получении информации об аккаунте.")


def register_account_handlers(bot: TeleBot):
    """Регистрирует обработчики управления аккаунтами."""
    
    @bot.message_handler(func=lambda message: message.text == '/account')
    def account_command(message):
        """Команда управления аккаунтом."""
        account_command_impl(bot, message)
    
    @bot.message_handler(func=lambda message: message.text == '✅ Создать аккаунт')
    def create_account_confirm(message):
        """Подтверждение создания нового аккаунта."""
        telegram_user = message.from_user.first_name
        
        try:
            logger.info(f"create_account_confirm: user={telegram_user}")
            
            # Запрашиваем никнейм
            bot.send_message(
                message.chat.id,
                "🎮 Введите игровой никнейм для нового аккаунта:",
                reply_markup=ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True).add(
                    KeyboardButton(f'Использовать {telegram_user}'),
                    KeyboardButton('❌ Отмена')
                )
            )
            
            # Устанавливаем состояние ожидания ввода ника
            state = get_user_state(telegram_user)
            state.desire = 'create_account'
            
        except Exception as e:
            logger.error(f"Error in create_account_confirm: {e}", exc_info=True)
    
    @bot.message_handler(func=lambda message: message.text == '➕ Создать новый аккаунт')
    def create_new_account_existing(message):
        """Создание нового аккаунта для существующего пользователя."""
        telegram_user = message.from_user.first_name
        
        try:
            logger.info(f"create_new_account_existing: user={telegram_user}")
            
            bot.send_message(
                message.chat.id,
                "⚠️ **Внимание!**\n\nСоздание нового аккаунта заменит ваш текущий профиль.\n"
                "Все данные текущего аккаунта будут сохранены в БД, но активным станет новый профиль.\n\n"
                "🎮 Введите никнейм для нового аккаунта:",
                reply_markup=ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True).add(
                    KeyboardButton('❌ Отмена')
                ),
                parse_mode='Markdown'
            )
            
            state = get_user_state(telegram_user)
            state.desire = 'create_new_account'
            
        except Exception as e:
            logger.error(f"Error in create_new_account_existing: {e}", exc_info=True)
    
    @bot.message_handler(func=lambda message: message.text.startswith('Использовать ') and get_user_state(message.from_user.first_name).desire == 'create_account')
    def use_telegram_name(message):
        """Использовать telegram имя как никнейм."""
        telegram_user = message.from_user.first_name
        state = get_user_state(telegram_user)
        
        try:
            logger.info(f"use_telegram_name: creating account for {telegram_user}")
            
            # Проверяем существует ли пользователь
            if db_manager.user_exists(telegram_user):
                # Пользователь уже есть - просто загружаем данные
                user_data = db_manager.get_user_data(telegram_user)
                if user_data:
                    state.name = user_data[1]
                    state.money = user_data[2]
                    from utils.helpers import string_to_animals_dict
                    state.count_dict = string_to_animals_dict(user_data[3])
                    logger.info(f"use_telegram_name: loaded existing user {telegram_user}, name={state.name}")
                else:
                    # Данные не найдены - устанавливаем дефолтные
                    state.name = telegram_user
                    state.money = 50000
                    logger.info(f"use_telegram_name: user exists but no data, setting defaults")
            else:
                # Создаем нового пользователя с начальным балансом 50000
                state.name = telegram_user
                state.money = 50000
                state.desire = ''
                
                db_manager.create_user(
                    us_name=telegram_user,
                    name=telegram_user,
                    money=50000
                )
                logger.info(f"use_telegram_name: created new user {telegram_user}")
            
            success_msg = f"✅ **Аккаунт успешно создан!**\n\n"
            success_msg += f"🎮 Никнейм: {telegram_user}\n"
            success_msg += f"💰 Начальный баланс: 50000 ₽\n\n"
            success_msg += f"Добро пожаловать в игру! 🎉"
            
            bot.send_message(message.chat.id, success_msg, parse_mode='Markdown')
            bot.send_message(
                message.chat.id,
                get_random_phrase(),
                reply_markup=get_help_keyboard()
            )
            
            logger.info(f"use_telegram_name: account created successfully")
        except Exception as e:
            logger.error(f"Error in use_telegram_name: {e}", exc_info=True)
            bot.send_message(message.chat.id, "Ошибка при создании аккаунта.")
    
    @bot.message_handler(func=lambda message: get_user_state(message.from_user.first_name).desire in ['create_account', 'create_new_account'] and message.text != '❌ Отмена')
    def process_nickname_input(message):
        """Обработка ввода никнейма для нового аккаунта."""
        telegram_user = message.from_user.first_name
        state = get_user_state(telegram_user)
        nickname = message.text.strip()
        
        try:
            logger.info(f"process_nickname_input: telegram_user={telegram_user}, nickname={nickname}")
            
            if len(nickname) < 2 or len(nickname) > 20:
                bot.send_message(
                    message.chat.id,
                    "❌ Никнейм должен быть от 2 до 20 символов. Попробуйте снова:",
                    reply_markup=ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True).add(
                        KeyboardButton('❌ Отмена')
                    )
                )
                return
            
            # Создаем новый аккаунт
            if state.desire == 'create_account':
                # Первый аккаунт
                state.name = nickname
                state.money = 50000
                state.desire = ''
                
                # Проверяем существует ли пользователь
                if db_manager.user_exists(telegram_user):
                    # Пользователь уже есть - загружаем данные
                    user_data = db_manager.get_user_data(telegram_user)
                    if user_data:
                        state.name = user_data[1]
                        state.money = user_data[2]
                        from utils.helpers import string_to_animals_dict
                        state.count_dict = string_to_animals_dict(user_data[3])
                        logger.info(f"process_nickname_input: loaded existing user {telegram_user}")
                else:
                    # Создаем нового
                    db_manager.create_user(
                        us_name=telegram_user,
                        name=nickname,
                        money=50000
                    )
                    logger.info(f"process_nickname_input: created new user {telegram_user}")
                
                success_msg = f"✅ **Аккаунт успешно создан!**\n\n"
                success_msg += f"🎮 Никнейм: {nickname}\n"
                success_msg += f"💰 Начальный баланс: 50000 ₽\n\n"
                success_msg += f"Добро пожаловать в игру! 🎉"
                
            else:
                # Новый аккаунт (замена существующего)
                # Создаем новую запись с уникальным ключом
                new_us_name = f"{telegram_user}_{nickname}"
                
                # Создаем новый state
                if new_us_name in user_states:
                    del user_states[new_us_name]
                
                new_state = get_user_state(new_us_name)
                new_state.name = nickname
                new_state.money = 50000
                
                db_manager.create_user(
                    us_name=new_us_name,
                    name=nickname,
                    money=50000
                )
                
                # Переключаем текущий state
                user_states[telegram_user] = new_state
                new_state.desire = ''
                
                success_msg = f"✅ **Новый аккаунт создан!**\n\n"
                success_msg += f"🎮 Никнейм: {nickname}\n"
                success_msg += f"💰 Начальный баланс: 50000 ₽\n\n"
                success_msg += f"Старый аккаунт сохранен в БД.\n"
                success_msg += f"Теперь активен новый профиль! 🎉"
            
            bot.send_message(message.chat.id, success_msg, parse_mode='Markdown')
            bot.send_message(
                message.chat.id,
                get_random_phrase(),
                reply_markup=get_help_keyboard()
            )
            
            logger.info(f"process_nickname_input: account created for {nickname}")
        except Exception as e:
            logger.error(f"Error in process_nickname_input: {e}", exc_info=True)
            bot.send_message(message.chat.id, "Ошибка при создании аккаунта.")
            state.desire = ''
    
    @bot.message_handler(func=lambda message: message.text == '✏️ Сменить ник')
    def change_nickname(message):
        """Обработчик смены никнейма."""
        telegram_user = message.from_user.first_name
        state = get_user_state(telegram_user)
        
        try:
            logger.info(f"change_nickname: user={telegram_user}")
            
            bot.send_message(
                message.chat.id,
                "✏️ Введите новый никнейм:\n\n(от 2 до 20 символов)",
                reply_markup=ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True).add(
                    KeyboardButton('❌ Отмена')
                )
            )
            
            state.desire = 'change_nickname'
            
        except Exception as e:
            logger.error(f"Error in change_nickname: {e}", exc_info=True)
    
    @bot.message_handler(func=lambda message: get_user_state(message.from_user.first_name).desire == 'change_nickname' and message.text != '❌ Отмена')
    def process_nickname_change(message):
        """Обработка изменения никнейма."""
        telegram_user = message.from_user.first_name
        state = get_user_state(telegram_user)
        new_nickname = message.text.strip()
        
        try:
            logger.info(f"process_nickname_change: user={telegram_user}, new_nickname={new_nickname}")
            
            if len(new_nickname) < 2 or len(new_nickname) > 20:
                bot.send_message(
                    message.chat.id,
                    "❌ Никнейм должен быть от 2 до 20 символов. Попробуйте снова:",
                    reply_markup=ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True).add(
                        KeyboardButton('❌ Отмена')
                    )
                )
                return
            
            # Обновляем никнейм
            old_nickname = state.name
            state.name = new_nickname
            state.desire = ''
            
            # Получаем текущие данные из БД для сохранения animals
            from utils.helpers import animals_dict_to_string
            animals_str = animals_dict_to_string(state.count_dict)
            
            # Обновляем в БД
            db_manager.update_user(
                us_name=telegram_user,
                name=new_nickname,
                money=state.money,
                animals=animals_str,
                ad_animals=''
            )
            
            success_msg = f"✅ **Никнейм успешно изменен!**\n\n"
            success_msg += f"📝 Старый никнейм: {old_nickname}\n"
            success_msg += f"✨ Новый никнейм: {new_nickname}\n"
            
            bot.send_message(message.chat.id, success_msg, parse_mode='Markdown')
            bot.send_message(
                message.chat.id,
                get_random_phrase(),
                reply_markup=get_help_keyboard()
            )
            
            logger.info(f"process_nickname_change: nickname changed from {old_nickname} to {new_nickname}")
        except Exception as e:
            logger.error(f"Error in process_nickname_change: {e}", exc_info=True)
            bot.send_message(message.chat.id, "Ошибка при изменении никнейма.")
            state.desire = ''
    
    @bot.message_handler(func=lambda message: message.text == '🗑 Удалить аккаунт')
    def delete_account_request(message):
        """Запрос на удаление аккаунта."""
        telegram_user = message.from_user.first_name
        state = get_user_state(telegram_user)
        
        try:
            logger.info(f"delete_account_request: user={telegram_user}")
            
            warning_msg = "⚠️ **ВНИМАНИЕ!**\n\n"
            warning_msg += "Вы собираетесь удалить свой аккаунт.\n"
            warning_msg += "Это действие необратимо!\n\n"
            warning_msg += f"🎮 Никнейм: {state.name}\n"
            warning_msg += f"💰 Баланс: {state.money} ₽\n\n"
            warning_msg += "Вы уверены?"
            
            markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup.add(KeyboardButton('✅ Да, удалить'))
            markup.add(KeyboardButton('❌ Отмена'))
            
            bot.send_message(message.chat.id, warning_msg, reply_markup=markup, parse_mode='Markdown')
            
            state.desire = 'delete_account_confirm'
            
        except Exception as e:
            logger.error(f"Error in delete_account_request: {e}", exc_info=True)
    
    @bot.message_handler(func=lambda message: message.text == '✅ Да, удалить' and get_user_state(message.from_user.first_name).desire == 'delete_account_confirm')
    def delete_account_confirm(message):
        """Подтверждение удаления аккаунта."""
        telegram_user = message.from_user.first_name
        state = get_user_state(telegram_user)
        
        try:
            logger.info(f"delete_account_confirm: deleting account for user={telegram_user}")
            
            old_nickname = state.name
            
            # Удаляем пользователя из БД
            db_manager.delete_user(telegram_user)
            
            # Очищаем state
            if telegram_user in user_states:
                del user_states[telegram_user]
            
            success_msg = f"✅ **Аккаунт удален**\n\n"
            success_msg += f"Аккаунт '{old_nickname}' был успешно удален.\n"
            success_msg += f"Вы можете создать новый аккаунт через кнопку Account."
            
            bot.send_message(message.chat.id, success_msg, parse_mode='Markdown')
            bot.send_message(
                message.chat.id,
                "Возвращайтесь снова! 👋",
                reply_markup=get_help_keyboard()
            )
            
            logger.info(f"delete_account_confirm: account deleted for {telegram_user}")
        except Exception as e:
            logger.error(f"Error in delete_account_confirm: {e}", exc_info=True)
            bot.send_message(message.chat.id, "Ошибка при удалении аккаунта.")
            state.desire = ''
    
    @bot.message_handler(func=lambda message: message.text == '❌ Отмена' and get_user_state(message.from_user.first_name).desire in ['create_account', 'create_new_account', 'change_nickname', 'delete_account_confirm', ''])
    def cancel_account_action(message):
        """Отмена действия с аккаунтом."""
        telegram_user = message.from_user.first_name
        state = get_user_state(telegram_user)
        
        try:
            logger.info(f"cancel_account_action: user={telegram_user}")
            state.desire = ''
            
            bot.send_message(
                message.chat.id,
                "↩️ Действие отменено.",
                reply_markup=get_help_keyboard()
            )
        except Exception as e:
            logger.error(f"Error in cancel_account_action: {e}", exc_info=True)
