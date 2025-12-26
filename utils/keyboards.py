"""Клавиатуры для телеграм-бота."""
from telebot import types


def get_registration_keyboard():
    """Клавиатура для регистрации."""
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    btn1 = types.KeyboardButton('Буду использовать свой стандартный ник')
    btn2 = types.KeyboardButton('Введу свой ник')
    markup.add(btn1, btn2)
    return markup


def get_confirmation_keyboard():
    """Клавиатура для подтверждения ника."""
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    btn1 = types.KeyboardButton('Да, ник - супер!')
    btn2 = types.KeyboardButton('Нет, надо по-другому')
    markup.add(btn1, btn2)
    return markup


def get_animals_keyboard():
    """Клавиатура для выбора животных (покупка)."""
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    btn1 = types.KeyboardButton('Корову')
    btn2 = types.KeyboardButton('Свинью')
    btn3 = types.KeyboardButton('Кролика')
    btn4 = types.KeyboardButton('Курицу')
    btn5 = types.KeyboardButton('Лошадь')
    btn6 = types.KeyboardButton('Овечку')
    btn7 = types.KeyboardButton('Гуся')
    btn_back = types.KeyboardButton('❌ Назад')
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
    markup.add(btn_back)
    return markup


def get_sell_keyboard():
    """Клавиатура для выбора товаров на продажу."""
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    btn1 = types.KeyboardButton('Корову')
    btn2 = types.KeyboardButton('Свинью')
    btn3 = types.KeyboardButton('Кролика')
    btn4 = types.KeyboardButton('Курицу')
    btn5 = types.KeyboardButton('Лошадь')
    btn6 = types.KeyboardButton('Овечку')
    btn7 = types.KeyboardButton('Гуся')
    btn8 = types.KeyboardButton('Овечью шерсть (кг)')
    btn9 = types.KeyboardButton('Куриные яйца (десятки)')
    btn10 = types.KeyboardButton('Коровье молоко (литры)')
    btn_back = types.KeyboardButton('❌ Назад')
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10)
    markup.add(btn_back)
    return markup


def get_help_keyboard():
    """Инлайн-клавиатура с основными командами."""
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Help', callback_data='/help')
    btn2 = types.InlineKeyboardButton(text='Account', callback_data='/account')
    btn3 = types.InlineKeyboardButton(text='Top', callback_data='/top')
    btn4 = types.InlineKeyboardButton(text='Costs', callback_data='/cost')
    btn5 = types.InlineKeyboardButton(text='Buy', callback_data='/buy')
    btn6 = types.InlineKeyboardButton(text='Myinfo', callback_data='/myinfo')
    btn7 = types.InlineKeyboardButton(text='Sell', callback_data='/sell')
    markup.add(btn1, btn2)
    markup.add(btn3, btn4, btn5)
    markup.add(btn6, btn7)
    return markup


def get_back_keyboard():
    """Простая клавиатура только с кнопкой Назад."""
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    btn_back = types.KeyboardButton('❌ Назад')
    markup.add(btn_back)
    return markup
