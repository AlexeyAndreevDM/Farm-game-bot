from telebot import types
import telebot
import datetime as dt
from random import randint
import sqlite3

time = dt.datetime.now().strftime("%A %d-%B-%y %H:%M:%S")
name, topplace, money = '', '', 50000
desire, animals, count, buyan, sell_it = '', ['Корову', 'Свинью', 'Кролика', 'Курицу', 'Лошадь', 'Овечку', 'Гуся'], 0, \
    '', ''
time = [50, 35, 5, 10, 65, 45, 10]
bot = telebot.TeleBot('6016919639:AAE6_gNV_1sjGN_wUBHAYyciJrAyl1uIeEA')
sell_dict = {'Корову': {1: randint(50000, 60000)},
             'Свинью': {1: randint(22000, 27000)},
             'Лошадь': {1: randint(120000, 150000)},
             'Кролика': {1: randint(800, 1000)},
             'Курицу': {1: randint(500, 800)},
             'Гуся': {1: randint(1900, 2100)},
             'Овечку': {1: randint(32000, 34000)},
             'Коровье молоко (литры)': {1: randint(80, 110), 100: randint(5000, 6000), 300: randint(10500, 12050),
                                        550: randint(14000, 15200)},
             'Куриные яйца (десятки)': {1: randint(80, 110), 50: randint(3450, 3700),
                                        100: randint(5900, 6200),
                                        200: randint(9950, 10450)},
             'Овечью шерсть (кг)': {0.5: randint(480, 550), 1: randint(900, 1020),
                                    5: randint(3900, 4150),
                                    50: randint(26700, 27350)}}
dict = {'Корову': randint(8500, 13000), 'Свинью': randint(4500, 7000), 'Кролика': randint(250, 450),
        'Курицу': randint(100, 250), 'Лошадь': randint(35000, 45000), 'Овечку': randint(6500, 8000),
        'Гуся': randint(450, 650)}
count_dict = {'Корову': 0, 'Свинью': 0, 'Кролика': 0, 'Курицу': 0, 'Лошадь': 0, 'Овечку': 0,
              'Гуся': 0}
products = {'Коровье молоко': 0, 'Куриные яйца': 0, 'Овечью шерсть': 0}
animals_names = ['Коров: ', 'Свиней: ', 'Кроликов: ', 'Куриц: ', 'Лошадей: ', 'Овечек: ', 'Гусей: ']
phrases = ['Судьба судьбой, но выбор всегда за тобой',
           'Ты — это то, что ты делаешь. Ты — это твой выбор. Тот, в кого себя превратишь.',
           'Когда стоишь перед выбором, просто подбрось монетку. Это не даст верного ответа, но в момент когда монетка'
           'в воздухе, ты уже знаешь на что надеешься',
           'В шахматах это называется «цугцванг», когда оказывается, что самый полезный ход — никуда не двигаться',
           'Правильного выбора в реальности не существует — есть только сделанный выбор и его последствия',
           'Наша жизнь это постоянный выбор: кому доверить свой безымянный палец, а кому средний']
us_name, anm, ad_anm = '', '', ''
add_animals = []


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    req = call.data.split('_')
    if req[0] == '/help':
        bot.send_message(call.message.chat.id,
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
        bot.send_message(call.message.chat.id, f"«{phrases[randint(0, len(phrases) - 1)]}»",
                         reply_markup=get_help_keyboard())
    elif req[0] == '/top':
        top(call.message)
    elif req[0] == '/cost':
        cost(call.message)
    elif req[0] == '/buy':
        buy(call.message)
    elif req[0] == '/myinfo':
        myinfo(call.message)
    elif req[0] == '/sell':
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
        bot.send_message(call.message.chat.id, f'Вот расценки для продаж:\n\n{s}')
        sell(call.message)


@bot.message_handler(commands=['start'])
def start_message(message):
    global us_name, name, money, anm, ad_anm
    us_name = message.from_user.first_name
    con = sqlite3.connect('farmers.db')
    cur = con.cursor()
    result = cur.execute('''SELECT us_name FROM goods''').fetchall()
    st = 0
    for i in result:
        if us_name in i:
            st = 1
            break
    name = cur.execute(f"SELECT name FROM goods WHERE us_name = ?;""", (us_name,)).fetchone()
    if name:
        name = name[0].strip()
    if st == 0 or name == '':
        bot.send_message(message.chat.id, f"Привет, {us_name}! "
                                          f"У тебя есть ферма и начальный капитал, тебе необходимо всячески "
                                          "развивать твое хозяйство, ведь это твой основной бизнес. Ты можешь покупать "
                                          "разных животных, от них идут непосредственно продукты, которые ты должен "
                                          "продавать, дабы зарабатывать и улучшаться, не забывай смотреть на"
                                          "расценки для твоих продаж, "
                                          "они меняются чуть ли не каждый день!  (возможно стоит купить 2 курицы, "
                                          "чем 1 корову ;) Каждый месяц будут подводится итоги и 3 лучших фермера "
                                          "получат соответствующего размера бонусы."
                                          "Словом, дерзайте! Команды: /help - Суть"
                                          " игры, /reg - регистрация,  /top - списки лучших фермеров,"
                                          "/cost - расценки на "
                                          "продукты, /buy - покупка животных, /myinfo - твоя основная информация"
                                          " /sell - продажа имеющихся продуктов.")
        bot.send_message(message.chat.id, f"«{phrases[randint(0, len(phrases) - 1)]}»",
                         reply_markup=get_help_keyboard())
    else:
        unpack = cur.execute(f"SELECT * FROM goods WHERE us_name = ?;""", (us_name,)).fetchall()[0]
        money, anm, ad_anm = unpack[2], unpack[3], unpack[4]

        bot.send_message(message.chat.id,
                         f"Привет, {name}! У тебя есть ферма и начальный капитал,"
                         f"тебе необходимо всячески "
                         "развивать твое хозяйство, ведь это твой основной бизнес. Ты можешь покупать "
                         "разных животных, от них идут непосредственно продукты, которые ты должен "
                         "продавать, дабы зарабатывать и улучшаться, не забывай смотреть на расценки для "
                         "твоих продаж, они меняются чуть ли не каждый день!  (возможно стоит купить 2 "
                         "курицы, чем 1 корову ;) Каждый месяц будут подводится итоги и 3 лучших фермера "
                         "получат соответствующего размера бонусы. Словом, дерзайте! Команды: /help - Суть"
                         " игры, /reg - регистрация,  /top - списки лучших фермеров, /cost - расценки для "
                         "покупки, /buy - покупка животных, /myinfo - твоя основная информация"
                         " /sell - продажа имеющихся продуктов.")
        bot.send_message(message.chat.id, f"«{phrases[randint(0, len(phrases) - 1)]}»",
                         reply_markup=get_help_keyboard())


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global name, buyan, money, desire, sell_it, animals_names, time
    if message.text == '/help':
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
