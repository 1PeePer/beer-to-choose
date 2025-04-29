# Product types
PRODUCT_TYPES = {
    "Пиво": "Пиво",
    "Сидр": "Сидр",
    "Медовуха": "Медовуха",
    "Напиток": "Напиток"  # Базовый тип для всех напитков
}

# Beer color types
BEER_COLOR_TYPES = {
    "светл": "Светлое",
    "темн": "Темное",
    "бел": "Светлое",  # Добавляем альтернативные варианты
    "черн": "Темное"
}

# Clarification types
CLARIFICATION_TYPES = {
    "осветл": "Осветленное",
    "неосветл": "Неосветленное"
}

# Alcohol types
ALCOHOL_TYPES = {
    "безалко": False
}

# Filtering types
FILTERING_TYPES = {
    "фильтр": "Фильтрованное",
    "нефильтр": "Нефильтрованное"
}

# Pasteurization types
PASTEURIZATION_TYPES = {
    "пастер": "Пастеризованное",
    "непастер": "Непастеризованное"
}

# Sweetness types
SWEETNESS_TYPES = {
    "сладк": "Сладкое",
    "полусладк": "Полусладкое",
    "полусух": "Полусухое",
    "сух": "Сухое"
}

# Packaging types
PACKAGING_TYPES = {
    "ж/б": "ж/б",
    "пэт": "ПЭТ",
    "с/б": "с/б"  # По умолчанию
}

# Alcohol percentage patterns
ALCOHOL_PERCENTAGE_PATTERNS = [
    r'(\d+[,.]?\d*)%',  # Просто процент
    r'не\s+менее\s+(\d+[,.]?\d*)%',  # Не менее X%
    r'не\s+более\s+(\d+[,.]?\d*)%',  # Не более X%
    r'от\s+(\d+[,.]?\d*)%',  # От X%
    r'до\s+(\d+[,.]?\d*)%'   # До X%
] 