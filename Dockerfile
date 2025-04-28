# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем зависимости для Playwright
RUN playwright install chromium
RUN playwright install-deps

# Копируем код проекта
COPY . .

# Создаем необходимые директории
RUN mkdir -p logs results

# Устанавливаем переменную окружения для Python
ENV PYTHONPATH=/app

# Запускаем shell для отладки
CMD ["/bin/bash"] 