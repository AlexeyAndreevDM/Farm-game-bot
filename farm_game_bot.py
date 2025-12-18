#!/usr/bin/env python3
"""
Farm Game Bot - Телеграм бот с симулятором фермы.

Модульная архитектура с разделением на компоненты:
- config: конфигурация и константы
- database: работа с базой данных
- handlers: обработчики команд и сообщений
- utils: вспомогательные функции
"""
import logging
import sys
import telebot

from config.settings import BOT_TOKEN
from handlers.start import register_start_handlers
from handlers.registration import register_registration_handlers
from handlers.shop import register_shop_handlers
from handlers.info import register_info_handlers
from handlers.callbacks import register_callback_handlers

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def main():
    """Главная функция запуска бота."""
    try:
        # Проверка наличия токена
        if not BOT_TOKEN:
            logger.error("BOT_TOKEN not found in environment variables!")
            sys.exit(1)
        
        # Инициализация бота
        bot = telebot.TeleBot(BOT_TOKEN)
        logger.info("Bot initialized successfully")
        
        # Регистрация обработчиков
        register_callback_handlers(bot)  # Должен быть первым
        register_start_handlers(bot)
        register_registration_handlers(bot)
        register_shop_handlers(bot)
        register_info_handlers(bot)
        
        logger.info("All handlers registered successfully")
        logger.info("Bot is starting...")
        
        # Запуск бота
        bot.polling(none_stop=True, interval=0)
        
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Critical error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
    bot.send_message(message.chat.id,
                        "У тебя есть ферма и начальный капитал, тебе необходимо всячески "
                        "развивать твое хозяйство, ведь это твой основной бизнес. Ты можешь покупать "
                        "разных животных, от них идут непосредственно продукты, которые ты должен "
                        "продавать, дабы зарабатывать и улучшаться, не забывай смотреть на расценки для "
                        "твоих продаж, они меняются чуть ли не каждый день!  (возможно стоит купить 2 "
                        "курицы, чем 1 корову ;) Каждый месяц будут подводится итоги и 3 лучших фермера "
                        "получат соответствующего размера бонусы. Словом, дерзайте! Команды: /help - Суть"
                        " игры, /reg - регистрация,  /top - списки лучших фермеров, /cost - расценки для "
                        "покупки, /buy - покупка животных, /myinfo - твоя основная информация"
                        " /sell - продажа имеющихся продуктов.")
elif message.text == '/reg':
    if name == '':
        msg = "Введи свой ник или используйте свой стандартный ник"
        bot.send_message(message.chat.id, msg, reply_markup=get_keyboard())
    else:
        bot.send_message(message.from_user.id, "Твой ник: " + name)
elif message.text == 'Буду использовать свой стандартный ник':
    name = us_name
    name_valid(message)
    save_account()
elif message.text == 'Введу свой ник':
    bot.register_next_step_handler(message, get_name)
elif message.text == 'Да, ник - супер!':
    name_valid(message)
    save_account()
elif message.text == 'Нет, надо по-другому':
    name_invalid(message)
elif message.text == '/myinfo':
    myinfo(message)
elif message.text == '/cost':
    cost(message)
elif message.text == '/sell':
    a, s = 0, ''
    for i in sell_dict:
        d = []
        if a <= len(sell_dict) - 4:
            for u in sell_dict[i]:
                d.append(str(u) + ': ' + str(sell_dict[i][u]) + 'руб')
            d = ', '.join(d)
            s += animals[a] + ': ' + d + "\n" + "\n"
        elif len(sell_dict) - 3 <= a < len(sell_dict) - 1:
            for u in sell_dict[i]:
                d.append(str(u) + ': ' + str(sell_dict[i][u]) + 'руб')
            d = ', '.join(d)
            s += i + ': ' + d + "\n" + "\n"
        else:
            for u in sell_dict[i]:
                d.append(str(u) + ': ' + str(sell_dict[i][u]) + ' руб')
            d = ', '.join(d)
            s += i + ': ' + d
        a += 1
    bot.send_message(message.chat.id, f'Вот расценки для продаж:\n\n{s}')
    sell(message)
elif message.text == '/buy':
    buy(message)
elif message.text == '/top':
    top(message)
elif message.text in animals and desire == 'buy':
    buyan = message.text
    if buyan == 'Корову':
        bot.send_photo(message.chat.id, "https://cdn.trinixy.ru/pics6/20191111/183958_2_trinixy_ru.jpg")
    elif buyan == 'Свинью':
        bot.send_photo(message.chat.id, "https://ria-glas.ru/wp-content/uploads/2022/08/chuma.jpg")
    elif buyan == 'Кролика':
        bot.send_photo(message.chat.id, "https://god-krolika.ru/wp-content/uploads/2022/06/1647186864_60-krot-info-p-smeshnie-milie-kroliki-smeshnie-foto-66.jpg")
    elif buyan == 'Курицу':
        bot.send_photo(message.chat.id, "https://krot.info/uploads/posts/2022-03/1646195172_59-krot-info-p-smeshnie-kuri-smeshnie-foto-62.png")
    elif buyan == 'Лошадь':
        bot.send_photo(message.chat.id, "https://i.pinimg.com/originals/dc/34/8d/dc348df97a3d7aef0003e1010fe4dfa3.jpg")
    elif buyan == 'Овечку':
        bot.send_photo(message.chat.id, "http://cdn.tomas-travel.com/germany/repository/GER00020060182526344/GER00020060004955376/GER00020060196171681.jpg")
    elif buyan == 'Гуся':
        bot.send_photo(message.chat.id, "https://kak2z.ru/my_img/img/2022/04/01/418d1.jpg")
    bot.send_message(message.chat.id, 'Сколько?')
elif message.text in sell_dict and desire == 'sell':
    sell_it = message.text
    if sell_it == 'Корову':
        bot.send_photo(message.chat.id, "https://agronom.media/wp-content/uploads/2019/01/pochemu-u-korovy-gorchit-moloko-9.jpg")
    elif sell_it == 'Свинью':
        bot.send_photo(message.chat.id, "https://funart.pro/uploads/posts/2021-12/1639619232_27-funart-pro-p-grustnaya-svinya-zhivotnie-krasivo-foto-29.jpg")
    elif sell_it == 'Кролика':
        bot.send_photo(message.chat.id, "https://i.pinimg.com/originals/5a/0c/24/5a0c243539ae471cb7a79b969fddff04.jpg")
    elif sell_it == 'Курицу':
        bot.send_photo(message.chat.id, "https://assets.change.org/photos/2/se/hx/pnSEhxmePrKidxR-1600x900-noPad.jpg?1544020894")
    elif sell_it == 'Лошадь':
        bot.send_photo(message.chat.id, "https://i.pinimg.com/originals/7a/a5/49/7aa5492e60da70a5f66d4d5c8f995923.jpg")
    elif sell_it == 'Овечку':
        bot.send_photo(message.chat.id, "https://get.pxhere.com/photo/grass-animal-wildlife-sheep-mammal-fauna-animals-vertebrate-sheeps-1191974.jpg")
    elif sell_it == 'Гуся':
        bot.send_photo(message.chat.id, "http://s3.fotokto.ru/photo/full/205/2055934.jpg")
    elif sell_it == 'Коровье молоко (литры)':
        bot.send_photo(message.chat.id, "https://i.pinimg.com/originals/af/3b/e1/af3be1025af5c88898841904b312792b.jpg")
    elif sell_it == 'Куриные яйца (десятки)':
        bot.send_photo(message.chat.id, "https://i.pinimg.com/originals/9a/c8/ad/9ac8ad0fbdef4f34ae24b7ec11ba0612.jpg")
    elif sell_it == 'Овечью шерсть (кг)':
        bot.send_photo(message.chat.id, "https://chert-poberi.ru/wp-content/uploads/proga2018/images/201906/igor2-15061913330233_2.jpg")
    bot.send_message(message.chat.id, f'Сколько вы хотите продать?')
elif desire == 'buy' and message.text.isdigit() and '.' not in list(message.text) \
        and 1 <= int(message.text) <= money // dict[buyan]:
    count_dict[buyan] += int(message.text)
    money -= dict[buyan] * int(message.text)
    bot.send_message(message.chat.id, f'Покупка произведена успешно! Ваш баланс: {money} '
                                        f'Время на ожидание взросления животного(ых) - '
                                        f'{time[animals.index(buyan)]} часов.')
    add_animals.append([buyan, message.text,
                        (dt.datetime.now() +
                            dt.timedelta(hours=time[animals.index(buyan)])).strftime("%A %d-%B-%y %H:%M:%S")])
    print(add_animals[0])
    # update_data()
    bot.send_message(message.chat.id, f"«{phrases[randint(0, len(phrases) - 1)]}»",
                        reply_markup=get_help_keyboard())
    desire = ''
else:
    if desire == 'buy':
        if not 1 <= int(message.text) <= money // dict[buyan] or '.' not in list(message.text):
            bot.send_message(message.chat.id, 'Введи количество корректно')
    if desire == 'sell':
        if sell_it in products:
            if int(message.text) > products[sell_it] or '.' not in list(message.text):
                bot.send_message(message.chat.id, 'Введи количество корректно')
        elif sell_it in count_dict:
            if int(message.text) > count_dict[sell_it] or '.' not in list(message.text):
                bot.send_message(message.chat.id, 'Введи количество корректно')


def myinfo(message):
    a, s = 0, ''
    topplace = 3
    for i in count_dict:
        if a != len(animals_names) - 1:
            if count_dict[i] != 0:
                s += animals_names[a] + str(count_dict[i]) + ' (растут)' + "\n"
            else:
                s += animals_names[a] + str(count_dict[i]) + "\n"
        else:
            if count_dict[i] != 0:
                s += animals_names[a] + str(count_dict[i]) + ' (растут)'
            else:
                s += animals_names[a] + str(count_dict[i])
        a += 1
    if name == '':
        bot.send_message(message.chat.id,
                         f"Твоя информация:\nНикнейм: {us_name}"
                         f"\nТвой бюджет: {money}\nТвое место в топе: {topplace}.\n{s}")
    else:
        bot.send_message(message.chat.id, f"Твоя информация:\nНикнейм: {name}\nТвой бюджет: {money}\nТвое место в топе:"
                                          f" {topplace}.\n{s}")
    bot.send_message(message.chat.id, f"«{phrases[randint(0, len(phrases) - 1)]}»",
                     reply_markup=get_help_keyboard())


def buy(message):
    global desire
    desire = 'buy'
    msg = f"Что хотите купить?"
    bot.send_message(message.chat.id, msg, reply_markup=get_keyboard2())


def top(message):
    topplace = 3
    if topplace == 1:
        congrat = 'ВЫ ТОП 1!'
        bot.send_message(message.chat.id, f'Так, посмотрим...\nВаш место в топе фермеров: {congrat}')
    else:
        bot.send_message(message.chat.id, f'Так, посмотрим...\nВаш место в топе фермеров: {topplace}')
    bot.send_message(message.chat.id, f"«{phrases[randint(0, len(phrases) - 1)]}»",
                     reply_markup=get_help_keyboard())


def cost(message):
    a = []
    for i in dict:
        a.append(dict[i])
    bot.send_message(message.chat.id, f"Расценки для покупки:\nКорова: {a[0]}\nСвинья: {a[1]}\nЛошадь: {a[4]}"
                                      f"\nКролик: {a[2]}\nКурица: {a[3]}\nГусь: {a[6]}\nОвечка: {a[5]}")
    bot.send_message(message.chat.id, f"«{phrases[randint(0, len(phrases) - 1)]}»",
                     reply_markup=get_help_keyboard())


def sell(message):
    global desire
    desire = 'sell'
    a = 0
    s = ''
    s += 'Вы можете продать:' + "\n"
    for i in count_dict:
        z = 0
        for y in add_animals:
            if buyan in y:
                z = 1
                break
        if a != len(animals_names) - 1 and count_dict[i] != 0 and z == 0:
            s += animals_names[a] + str(count_dict[i]) + "\n"
        elif z == 0:
            if count_dict[i] != 0:
                s += animals_names[a] + str(count_dict[i])
        a += 1
    bot.send_message(message.chat.id, s)
    msg = f"Что хотите продать?"
    bot.send_message(message.chat.id, msg, reply_markup=get_keyboard3())


def get_name(message):
    global name
    name = message.text
    msg = f"Твоя информация:\nНикнейм: {message.text}.\nТочно?"
    bot.send_message(message.chat.id, msg, reply_markup=get_keyboard1())


def get_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    btn1 = types.KeyboardButton('Буду использовать свой стандартный ник')
    btn2 = types.KeyboardButton('Введу свой ник')
    markup.add(btn1, btn2)
    return markup


def get_keyboard1():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    btn1 = types.KeyboardButton('Да, ник - супер!')
    btn2 = types.KeyboardButton('Нет, надо по-другому')
    markup.add(btn1, btn2)
    return markup


def get_keyboard2():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    btn1 = types.KeyboardButton('Корову')
    btn2 = types.KeyboardButton('Свинью')
    btn3 = types.KeyboardButton('Кролика')
    btn4 = types.KeyboardButton('Курицу')
    btn5 = types.KeyboardButton('Лошадь')
    btn6 = types.KeyboardButton('Овечку')
    btn7 = types.KeyboardButton('Гуся')
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
    return markup


def get_keyboard3():
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
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10)
    return markup


def get_help_keyboard():
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Help', callback_data='/help')
    # btn2 = types.InlineKeyboardButton(text='Reg', callback_data='/reg')
    btn3 = types.InlineKeyboardButton(text='Top', callback_data='/top')
    btn4 = types.InlineKeyboardButton(text='Costs', callback_data='/cost')
    btn5 = types.InlineKeyboardButton(text='Buy', callback_data='/buy')
    btn6 = types.InlineKeyboardButton(text='Myinfo', callback_data='/myinfo')
    btn7 = types.InlineKeyboardButton(text='Sell', callback_data='/sell')
    markup.add(btn1, btn3, btn4, btn5, btn6, btn7)
    return markup


def name_invalid(message):
    bot.send_message(message.chat.id, 'Введи свой ник корректно пожалуйста.')
    bot.register_next_step_handler(message, get_name)


def name_valid(message):
    bot.send_message(message.chat.id, 'Твой ник сохранен.')
    bot.send_message(message.chat.id, f"«{phrases[randint(0, len(phrases) - 1)]}»",
                     reply_markup=get_help_keyboard())


def save_account():
    con = sqlite3.connect("farmers.db")
    cur = con.cursor()
    a, anm, ad_anm = 0, '', ''
    for i in count_dict:
        if a != len(animals_names) - 1:
            anm += str(count_dict[i]) + ' '
        else:
            anm += str(count_dict[i])
        a += 1
    cur.execute(f"INSERT INTO goods VALUES(?,?,?,?,?)",
                (us_name, name, money, anm, ad_anm))
    con.commit()


def update_data():
    con = sqlite3.connect("farmers.db")
    cur = con.cursor()
    a, anm, ad_anm = 0, '', ''
    for i in count_dict:
        if a != len(animals_names) - 1:
            anm += str(count_dict[i]) + ' '
        else:
            anm += str(count_dict[i])
        a += 1
    cur.execute(f"UPDATE goods SET name = ?, money = ?, animals = ?, ad_animals = ? WHERE us_name = ?;",
                (name, money, anm, ad_anm, us_name,))
    con.commit()


bot.polling()
