from typing import Tuple, Optional, Dict
import re
from config.product_types import (
    PRODUCT_TYPES,
    BEER_COLOR_TYPES,
    CLARIFICATION_TYPES,
    ALCOHOL_TYPES,
    FILTERING_TYPES,
    PASTEURIZATION_TYPES,
    SWEETNESS_TYPES,
    PACKAGING_TYPES,
    ALCOHOL_PERCENTAGE_PATTERNS
)

def process_product_name(name: str) -> Tuple[str, str, Optional[str], bool, Optional[str], Optional[str], Optional[Dict[str, float]], Optional[str], str, Optional[str]]:
    """
    Process product name to extract product type, color, alcohol status, filtering and pasteurization status.
    Returns tuple of (product_type, cleaned_name, color_type, is_alcoholic, filtering_type, pasteurization_type, alcohol_percentage, sweetness_type, packaging_type, clarification_type)
    """
    try:
        # Split name by spaces and check first word
        words = name.split()
        if not words:
            return "Неизвестный тип", name, None, True, None, None, None, None, PACKAGING_TYPES["с/б"], None

        first_word = words[0].lower()
        color_type = None
        is_alcoholic = True  # По умолчанию все товары алкогольные
        filtering_type = None
        pasteurization_type = None
        alcohol_percentage = None
        sweetness_type = None
        packaging_type = PACKAGING_TYPES["с/б"]  # По умолчанию стеклянная бутылка
        clarification_type = None
        
        # Проверяем, является ли первое слово названием бренда (начинается с заглавной буквы)
        if first_word[0].isupper():
            # Если первое слово - бренд, ищем тип товара в следующих словах
            for i, word in enumerate(words[1:], 1):
                if word.lower() in [t.lower() for t in PRODUCT_TYPES.values()]:
                    product_type = word
                    cleaned_name = " ".join(words[:i] + words[i+1:]).strip()
                    break
            else:
                # Если тип не найден, считаем что это пиво
                product_type = "Пиво"
                cleaned_name = name
        else:
            # Check for "Напиток" type
            if first_word == "напиток" and len(words) >= 2:
                # Get the next word as the drink type
                drink_type = words[1].lower()
                # Remove both words from name
                cleaned_name = " ".join(words[2:]).strip()
                product_type = f"Напиток {drink_type}"
            else:
                # Check other product types
                for product_type in PRODUCT_TYPES.values():
                    if first_word == product_type.lower():
                        # Remove product type from name and clean up
                        cleaned_name = " ".join(words[1:]).strip()
                        break
                else:
                    return "Неизвестный тип", name, None, True, None, None, None, None, PACKAGING_TYPES["с/б"], None

        # Check for color type in the cleaned name
        name_lower = cleaned_name.lower()
        for color_key, color_value in BEER_COLOR_TYPES.items():
            if re.search(rf'\b{color_key}[а-я]*\b', name_lower):
                color_type = color_value
                # Remove color type from name
                cleaned_name = re.sub(rf'\b{color_key}[а-я]*\b', '', cleaned_name, flags=re.IGNORECASE).strip()
                break

        # Check for clarification type in the cleaned name
        for clarification_key, clarification_value in CLARIFICATION_TYPES.items():
            if re.search(rf'\b{clarification_key}[а-я]*\b', name_lower):
                clarification_type = clarification_value
                # Remove clarification type from name
                cleaned_name = re.sub(rf'\b{clarification_key}[а-я]*\b', '', cleaned_name, flags=re.IGNORECASE).strip()
                break

        # Check for alcohol type in the cleaned name
        for alcohol_key, alcohol_value in ALCOHOL_TYPES.items():
            if re.search(rf'\b{alcohol_key}[а-я]*\b', name_lower):
                is_alcoholic = alcohol_value
                # Remove alcohol type from name
                cleaned_name = re.sub(rf'\b{alcohol_key}[а-я]*\b', '', cleaned_name, flags=re.IGNORECASE).strip()
                break

        # Check for filtering type in the cleaned name
        for filter_key, filter_value in FILTERING_TYPES.items():
            if re.search(rf'\b{filter_key}[а-я]*\b', name_lower):
                filtering_type = filter_value
                # Remove filtering type from name
                cleaned_name = re.sub(rf'\b{filter_key}[а-я]*\b', '', cleaned_name, flags=re.IGNORECASE).strip()
                break

        # Check for pasteurization type in the cleaned name
        for pasteur_key, pasteur_value in PASTEURIZATION_TYPES.items():
            if re.search(rf'\b{pasteur_key}[а-я]*\b', name_lower):
                pasteurization_type = pasteur_value
                # Remove pasteurization type from name
                cleaned_name = re.sub(rf'\b{pasteur_key}[а-я]*\b', '', cleaned_name, flags=re.IGNORECASE).strip()
                break

        # Check for sweetness type in the cleaned name
        for sweetness_key, sweetness_value in SWEETNESS_TYPES.items():
            if re.search(rf'\b{sweetness_key}[а-я]*\b', name_lower):
                sweetness_type = sweetness_value
                # Remove sweetness type from name
                cleaned_name = re.sub(rf'\b{sweetness_key}[а-я]*\b', '', cleaned_name, flags=re.IGNORECASE).strip()
                break

        # Check for packaging type in the cleaned name
        for packaging_key, packaging_value in PACKAGING_TYPES.items():
            if re.search(rf'\b{packaging_key}\b', name_lower):
                packaging_type = packaging_value
                # Remove packaging type from name
                cleaned_name = re.sub(rf'\b{packaging_key}\b', '', cleaned_name, flags=re.IGNORECASE).strip()
                break

        # Extract alcohol percentage
        for pattern in ALCOHOL_PERCENTAGE_PATTERNS:
            match = re.search(pattern, name_lower)
            if match:
                percentage = float(match.group(1).replace(',', '.'))
                alcohol_percentage = percentage
                break

        # Remove alcohol percentage and related words from name
        cleaned_name = re.sub(r'\d+[,.]?\d*%', '', cleaned_name).strip()
        cleaned_name = re.sub(r'не\s+менее\s+\d+[,.]?\d*%', '', cleaned_name).strip()
        cleaned_name = re.sub(r'не\s+более\s+\d+[,.]?\d*%', '', cleaned_name).strip()
        cleaned_name = re.sub(r'от\s+\d+[,.]?\d*%', '', cleaned_name).strip()
        cleaned_name = re.sub(r'до\s+\d+[,.]?\d*%', '', cleaned_name).strip()
        
        # Remove remaining words related to alcohol percentage
        cleaned_name = re.sub(r'\bне\s+менее\b', '', cleaned_name, flags=re.IGNORECASE).strip()
        cleaned_name = re.sub(r'\bне\s+более\b', '', cleaned_name, flags=re.IGNORECASE).strip()
        cleaned_name = re.sub(r'\bот\b', '', cleaned_name, flags=re.IGNORECASE).strip()
        cleaned_name = re.sub(r'\bдо\b', '', cleaned_name, flags=re.IGNORECASE).strip()

        # Удаляем лишние запятые и пробелы
        # Заменяем все запятые и точки на пробелы
        cleaned_name = re.sub(r'[,.]', ' ', cleaned_name)
        # Нормализуем все пробелы (удаляем множественные пробелы)
        cleaned_name = re.sub(r'\s+', ' ', cleaned_name).strip()

        # Удаляем цифру 0 в конце названия
        cleaned_name = re.sub(r'\s*0\s*$', '', cleaned_name).strip()

        # Удаляем "алк" из названия
        cleaned_name = re.sub(r'\bалк\b', '', cleaned_name, flags=re.IGNORECASE).strip()
        
        # Удаляем множественные точки
        cleaned_name = re.sub(r'\.+', '.', cleaned_name).strip()
        # Удаляем точку в конце названия
        cleaned_name = re.sub(r'\.$', '', cleaned_name).strip()

        return product_type, cleaned_name, color_type, is_alcoholic, filtering_type, pasteurization_type, alcohol_percentage, sweetness_type, packaging_type, clarification_type
        
    except Exception as e:
        logging.warning(f"Error processing product name: {str(e)}") # type: ignore
        return "Неизвестный тип", name, None, True, None, None, None, None, PACKAGING_TYPES["с/б"], None 