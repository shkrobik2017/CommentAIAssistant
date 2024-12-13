# Используем Python 3.11 как базовый образ
FROM python:3.11

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем Poetry
RUN pip install --no-cache-dir poetry

# Копируем только файлы зависимостей для кэширования
COPY pyproject.toml poetry.lock /app/

# Устанавливаем зависимости напрямую
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes \
    && pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . /app

# Команда по умолчанию для запуска приложения
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]