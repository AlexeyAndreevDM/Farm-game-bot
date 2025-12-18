"""Настройки и константы бота."""
import os





































































































































price_manager = PriceManager()# Глобальный экземпляр менеджера цен        return f"{hours}ч {minutes}мин"                minutes = int((time_left.total_seconds() % 3600) // 60)        hours = int(time_left.total_seconds() // 3600)                    return "скоро"        if time_left.total_seconds() <= 0:                time_left = next_update - dt.datetime.now()        next_update = self.last_update + dt.timedelta(hours=PRICE_UPDATE_INTERVAL_HOURS)                    return "неизвестно"        if not self.last_update:        """Получить время до следующего обновления цен."""    def get_time_until_update(self) -> str:            self._generate_new_prices()        logger.info("Force updating prices")        """Принудительное обновление цен (для администратора)."""    def force_update(self):            return self.sell_prices            self._generate_new_prices()            logger.info("Auto-updating prices")        if self._should_update_prices():        """Получить актуальные цены на продажу."""    def get_sell_prices(self) -> Dict:            return self.animal_prices            self._generate_new_prices()            logger.info("Auto-updating prices")        if self._should_update_prices():        """Получить актуальные цены на покупку животных."""    def get_animal_prices(self) -> Dict:            return next_update.strftime("%d.%m.%Y %H:%M")        next_update = self.last_update + dt.timedelta(hours=PRICE_UPDATE_INTERVAL_HOURS)            return "неизвестно"        if not self.last_update:        """Получение времени следующего обновления."""    def _get_next_update_time(self) -> str:                logger.error(f"Error saving prices to cache: {e}")        except Exception as e:            logger.info("Prices saved to cache")                json.dump(data, f, ensure_ascii=False, indent=2)            with open(PRICES_FILE, 'w', encoding='utf-8') as f:            }                'last_update': self.last_update.isoformat()                'sell_prices': self.sell_prices,                'animal_prices': self.animal_prices,            data = {        try:        """Сохранение цен в кэш."""    def _save_prices(self):            logger.info(f"Generated new prices. Next update: {self._get_next_update_time()}")                    logger.error(f"Error updating total_assets: {e}")        except Exception as e:            logger.info("Updated total_assets for all players after price change")            db_manager.update_all_total_assets(self.animal_prices, self.sell_prices)            from database.db_manager import db_manager        try:        # Обновляем total_assets для всех игроков                self._save_prices()        self.last_update = dt.datetime.now()        self.sell_prices = get_sell_prices()        self.animal_prices = get_animal_prices()        """Генерация новых цен."""    def _generate_new_prices(self):            return time_since_update.total_seconds() >= PRICE_UPDATE_INTERVAL_HOURS * 3600        time_since_update = dt.datetime.now() - self.last_update                    return True        if not self.last_update:        """Проверка, нужно ли обновлять цены."""    def _should_update_prices(self) -> bool:            self._generate_new_prices()        # Если файла нет или произошла ошибка, генерируем новые цены                        logger.error(f"Error loading prices from cache: {e}")            except Exception as e:                            return                            logger.info(f"Loaded prices from cache. Next update: {self._get_next_update_time()}")                        else:                            self._generate_new_prices()                            logger.info("Prices are outdated, generating new ones")                        if self._should_update_prices():                        # Проверяем, нужно ли обновить цены                                                self.last_update = dt.datetime.fromisoformat(last_update_str)                    if last_update_str:                                        last_update_str = data.get('last_update')                    self.sell_prices = data.get('sell_prices', {})                    self.animal_prices = data.get('animal_prices', {})                    data = json.load(f)                with open(PRICES_FILE, 'r', encoding='utf-8') as f:            try:        if os.path.exists(PRICES_FILE):        """Загрузить цены из кэша или сгенерировать новые."""    def _load_or_generate_prices(self):            self._load_or_generate_prices()        self.last_update = None        self.sell_prices = {}        self.animal_prices = {}        """Инициализация менеджера цен."""    def __init__(self):        """Класс для управления ценами с автоматическим обновлением."""class PriceManager:PRICES_FILE = 'prices_cache.json'logger = logging.getLogger(__name__)from config.settings import get_animal_prices, get_sell_prices, PRICE_UPDATE_INTERVAL_HOURSfrom typing import Dictimport osimport jsonimport datetime as dtfrom random import randint
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

# Частота обновления цен (в часах)
PRICE_UPDATE_INTERVAL_HOURS = 24

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
