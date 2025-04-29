# Beer Parser API

API для парсинга и управления данными о пивных продуктах.

## Установка

1. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
venv\Scripts\activate     # для Windows
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

## Запуск

```bash
uvicorn parser_api.api.main:app --reload
```

API будет доступно по адресу: http://localhost:8000

## Документация

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Эндпоинты

### GET /api/v1/products
Получить список всех продуктов.

### POST /api/v1/update
Обновить данные продуктов.

Параметры:
- address: str - адрес магазина

## Логирование

Логи сохраняются в директории `logs/api.log`

## Разработка

1. Установите зависимости для разработки:
```bash
pip install -r requirements-dev.txt
```

2. Запустите тесты:
```bash
pytest
``` 