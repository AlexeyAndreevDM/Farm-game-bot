"""Вспомогательные функции."""
import logging
from random import randint, choice
from config.settings import PHRASES, ANIMALS, ANIMALS_NAMES

logger = logging.getLogger(__name__)


def get_random_phrase() -> str:
    """Возвращает случайную мотивационную фразу."""
    return f"«{choice(PHRASES)}»"


def format_animals_string(count_dict: dict, add_animals: list = None) -> str:
    """Форматирует строку с количеством животных."""
    result = []
    for i, animal in enumerate(ANIMALS):
        animal_key = animal
        count = count_dict.get(animal_key, 0)
        
        is_growing = False
        if add_animals:
            for growing in add_animals:
                if animal in growing:
                    is_growing = True
                    break
        
        if i != len(ANIMALS_NAMES) - 1:
            if count != 0 and is_growing:
                result.append(f"{ANIMALS_NAMES[i]}{count} (растут)")
            else:
                result.append(f"{ANIMALS_NAMES[i]}{count}")
        else:
            if count != 0 and is_growing:
                result.append(f"{ANIMALS_NAMES[i]}{count} (растут)")
            else:
                result.append(f"{ANIMALS_NAMES[i]}{count}")
    
    return "\n".join(result)


def animals_dict_to_string(count_dict: dict) -> str:
    """Преобразует словарь с животными в строку для БД."""
    result = []
    for animal in ANIMALS:
        result.append(str(count_dict.get(animal, 0)))
    return ' '.join(result)


def string_to_animals_dict(animals_str: str) -> dict:
    """Преобразует строку из БД в словарь с животными."""
    if not animals_str or animals_str.strip() == '':
        return {animal: 0 for animal in ANIMALS}
    
    try:
        counts = animals_str.strip().split()
        result = {}
        for i, animal in enumerate(ANIMALS):
            result[animal] = int(counts[i]) if i < len(counts) else 0
        return result
    except (ValueError, IndexError) as e:
        logger.error(f"Error parsing animals string: {e}")
        return {animal: 0 for animal in ANIMALS}


def format_sell_prices(sell_dict: dict) -> str:
    """Форматирует строку с ценами на продажу."""
    result = []
    
    for i, key in enumerate(sell_dict):
        prices = []
        for amount, price in sell_dict[key].items():
            if i <= len(sell_dict) - 4:
                prices.append(f"{amount}: {price}руб")
            else:
                prices.append(f"{amount}: {price} руб")
        
        prices_str = ', '.join(prices)
        
        if i <= len(sell_dict) - 4:
            result.append(f"{ANIMALS[i]}: {prices_str}\n")
        elif len(sell_dict) - 3 <= i < len(sell_dict) - 1:
            result.append(f"{key}: {prices_str}\n")
        else:
            result.append(f"{key}: {prices_str}")
    
    return '\n'.join(result)


def validate_amount_input(text: str, max_amount: int = None) -> tuple[bool, int]:
    """
    Проверяет корректность введенного количества.
    
    Returns:
        tuple: (is_valid, amount)
    """
    try:
        if '.' in text:
            return False, 0
        
        amount = int(text)
        
        if amount < 1:
            return False, 0
        
        if max_amount is not None and amount > max_amount:
            return False, 0
        
        return True, amount
    except ValueError:
        return False, 0
