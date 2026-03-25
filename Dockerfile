# Используем легковесный образ Python
FROM python:3.12-slim

# Устанавливаем переменные окружения, чтобы Python не кешировал байт-код и сразу выводил логи
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_DEBUG=0
ENV DJANGO_SECRET_KEY=QT4qDcSkqGyiBp0cKWYP0k8RGj9X_bHHDHjrfcaPLaKqyIS2z7dpcRJcy5Vf0lfV4wk
ENV ALLOWED_HOSTS=tutorsite-9axt.onrender.com

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
RUN chmod +x /app/start.sh

# Собираем статику (опционально, если будешь использовать Nginx)
# RUN python manage.py collectstatic --noinput

# Открываем порт 8000
EXPOSE 8000

# Команда для запуска (migrate + collectstatic + gunicorn)
CMD ["/app/start.sh"]
