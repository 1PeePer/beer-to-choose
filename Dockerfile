# Используем официальный образ Python
FROM python:3.13.3-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем зависимости для Playwright
RUN playwright install chromium
RUN playwright install-deps

# Копируем код проекта
COPY parser_api/ parser_api/

# Создаем необходимые директории
RUN mkdir -p logs results

# Устанавливаем переменную окружения для Python
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Запускаем приложение
CMD ["uvicorn", "parser_api.api.main:app", "--host", "0.0.0.0", "--port", "8000"] 