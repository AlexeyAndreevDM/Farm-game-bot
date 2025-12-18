"""Настройки и константы бота."""
import os
from random import randint
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Конфигурация бота
BOT_TOKEN = os.getenv('BOT_TOKEN', '')
DB_NAME = os.getenv('DB_NAME', 'farmers.db')

# Начальный капитал
INITIAL_MONEY = 50000

# Животные
ANIMALS = ['Корову', 'Свинью', 'Кролика', 'Курицу', 'Лошадь', 'Овечку', 'Гуся']
ANIMALS_NAMES = ['Коров: ', 'Свиней: ', 'Кроликов: ', 'Куриц: ', 'Лошадей: ', 'Овечек: ', 'Гусей: ']

# Время взросления животных (часы)
ANIMALS_GROW_TIME = {
    'Корову': 50,
    'Свинью': 35,
    'Кролика': 5,
    'Курицу': 10,
    'Лошадь': 65,
    'Овечку': 45,
    'Гуся': 10
}

# Продукты
PRODUCTS = ['Коровье молоко', 'Куриные яйца', 'Овечью шерсть']

# Цены на покупку животных (случайные в диапазоне)
def get_animal_prices():
    """Генерирует случайные цены на животных."""
    return {
        'Корову': randint(8500, 13000),
        'Свинью': randint(4500, 7000),
        'Кролика': randint(250, 450),
        'Курицу': randint(100, 250),
        'Лошадь': randint(35000, 45000),
        'Овечку': randint(6500, 8000),
        'Гуся': randint(450, 650)
    }

# Цены на продажу животных и продуктов (случайные в диапазоне)
def get_sell_prices():
    """Генерирует случайные цены на продажу."""
    return {
        'Корову': {1: randint(50000, 60000)},
        'Свинью': {1: randint(22000, 27000)},
        'Лошадь': {1: randint(120000, 150000)},
        'Кролика': {1: randint(800, 1000)},
        'Курицу': {1: randint(500, 800)},
        'Гуся': {1: randint(1900, 2100)},
        'Овечку': {1: randint(32000, 34000)},
        'Коровье молоко (литры)': {
            1: randint(80, 110),
            100: randint(5000, 6000),
            300: randint(10500, 12050),
            550: randint(14000, 15200)
        },
        'Куриные яйца (десятки)': {
            1: randint(80, 110),
            50: randint(3450, 3700),
            100: randint(5900, 6200),
            200: randint(9950, 10450)
        },
        'Овечью шерсть (кг)': {
            0.5: randint(480, 550),
            1: randint(900, 1020),
            5: randint(3900, 4150),
            50: randint(26700, 27350)
        }
    }

# URL изображений животных
ANIMAL_IMAGES = {
    'Корову': "https://cdn.trinixy.ru/pics6/20191111/183958_2_trinixy_ru.jpg",
    'Свинью': "https://ria-glas.ru/wp-content/uploads/2022/08/chuma.jpg",
    'Кролика': "https://god-krolika.ru/wp-content/uploads/2022/06/1647186864_60-krot-info-p-smeshnie-milie-kroliki-smeshnie-foto-66.jpg",
    'Курицу': "https://krot.info/uploads/posts/2022-03/1646195172_59-krot-info-p-smeshnie-kuri-smeshnie-foto-62.png",
    'Лошадь': "https://i.pinimg.com/originals/dc/34/8d/dc348df97a3d7aef0003e1010fe4dfa3.jpg",
    'Овечку': "http://cdn.tomas-travel.com/germany/repository/GER00020060182526344/GER00020060004955376/GER00020060196171681.jpg",
    'Гуся': "https://kak2z.ru/my_img/img/2022/04/01/418d1.jpg"
}

# URL изображений для продажи
SELL_IMAGES = {
    'Корову': "https://agronom.media/wp-content/uploads/2019/01/pochemu-u-korovy-gorchit-moloko-9.jpg",
    'Свинью': "https://funart.pro/uploads/posts/2021-12/1639619232_27-funart-pro-p-grustnaya-svinya-zhivotnie-krasivo-foto-29.jpg",
    'Кролика': "https://i.pinimg.com/originals/5a/0c/24/5a0c243539ae471cb7a79b969fddff04.jpg",
    'Курицу': "https://assets.change.org/photos/2/se/hx/pnSEhxmePrKidxR-1600x900-noPad.jpg?1544020894",
    'Лошадь': "https://i.pinimg.com/originals/7a/a5/49/7aa5492e60da70a5f66d4d5c8f995923.jpg",
    'Овечку': "https://get.pxhere.com/photo/grass-animal-wildlife-sheep-mammal-fauna-animals-vertebrate-sheeps-1191974.jpg",
    'Гуся': "http://s3.fotokto.ru/photo/full/205/2055934.jpg",
    'Коровье молоко (литры)': "https://i.pinimg.com/originals/af/3b/e1/af3be1025af5c88898841904b312792b.jpg",
    'Куриные яйца (десятки)': "https://i.pinimg.com/originals/9a/c8/ad/9ac8ad0fbdef4f34ae24b7ec11ba0612.jpg",
    'Овечью шерсть (кг)': "https://chert-poberi.ru/wp-content/uploads/proga2018/images/201906/igor2-15061913330233_2.jpg"
}

# Мотивационные фразы
PHRASES = [
    'Судьба судьбой, но выбор всегда за тобой',
    'Ты — это то, что ты делаешь. Ты — это твой выбор. Тот, в кого себя превратишь.',
    'Когда стоишь перед выбором, просто подбрось монетку. Это не даст верного ответа, но в момент когда монетка в воздухе, ты уже знаешь на что надеешься',
    'В шахматах это называется «цугцванг», когда оказывается, что самый полезный ход — никуда не двигаться',
    'Правильного выбора в реальности не существует — есть только сделанный выбор и его последствия',
    'Наша жизнь это постоянный выбор: кому доверить свой безымянный палец, а кому средний'
]
