FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

# Собираем статику для WhiteNoise
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Daphne: HTTP + WebSocket
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "config.asgi:application"]