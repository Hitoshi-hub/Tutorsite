# Используем легковесный образ Python
FROM python:3.12-slim

# Устанавливаем переменные окружения, чтобы Python не кешировал байт-код и сразу выводил логи
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Устанавливаем системные зависимости для Pillow и работы с БД
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Создаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . /app/

# Собираем статику (опционально, если будешь использовать Nginx)
# RUN python manage.py collectstatic --noinput

# Открываем порт 8000
EXPOSE 8000

# Команда для запуска (используем gunicorn для продакшн-подобной среды или runserver для теста)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]