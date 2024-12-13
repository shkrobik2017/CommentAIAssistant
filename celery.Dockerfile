# Используем Python 3.11 как базовый образ
FROM python:3.11

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем Poetry
RUN pip install --no-cache-dir poetry

# Копируем только файлы зависимостей для кэширования
COPY pyproject.toml poetry.lock /app/

# Устанавливаем зависимости через Poetry
RUN poetry install --no-root --no-interaction

# Копируем весь проект
COPY . /app

# Команда для запуска FastAPI приложения и Celery воркера
CMD ["python", "-m", "celery", "-A", "celery_app.config.app_celery", "worker", "--loglevel=info"]
