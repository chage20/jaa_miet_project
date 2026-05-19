import os
import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


PROXY_URL = os.environ.get('HTTP_PROXY', '')
HAPP_PROXY = {
    'http': PROXY_URL,
    'https': PROXY_URL,
} if PROXY_URL else {}


def send_registration_notification(user):
    """Отправляет уведомление в Telegram о новом пользователе."""
    if not settings.TELEGRAM_BOT_TOKEN or not settings.TELEGRAM_CHAT_ID:
        logger.warning("Telegram credentials not configured.")
        return

    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    text = (
        f"<b>Новая регистрация на сайте JAA!</b>\n"
        f"<b>Имя:</b> {user.first_name}\n"
        f"<b>Фамилия:</b> {user.last_name}\n"
        f"<b>Email:</b> {user.email}\n"
        f"<b>Город:</b> {user.city}\n"
        f"<b>Логин:</b> {user.username}"
    )

    payload = {
        "chat_id": settings.TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }

    try:
        response = requests.post(
            url,
            json=payload,
            timeout=15,
            proxies=HAPP_PROXY if HAPP_PROXY else None
        )
        response.raise_for_status()
        logger.info(f"Telegram notification sent for {user.username}")
    except requests.RequestException as e:
        logger.error(f"Telegram notification failed: {e}")