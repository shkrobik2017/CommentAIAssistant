# Используем Python 3.10 как базовый образ
FROM python:3.11

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем Poetry
RUN pip install --no-cache-dir poetry \
    && poetry self add poetry-plugin-export

# Копируем только файлы с зависимостями для кэширования сборки
COPY pyproject.toml poetry.lock /app/

# Export dependencies from Poetry to requirements.txt
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Копируем весь проект
COPY . /app

# Команда по умолчанию для запуска приложения
CMD ["poetry", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]