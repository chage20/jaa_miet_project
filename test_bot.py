import os
import sys
import requests

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "").strip()

PROXIES = {
    'http': 'http://127.0.0.1:10809',
    'https': 'http://127.0.0.1:10809',
}

if not BOT_TOKEN or not CHAT_ID:
    print("Ошибка: Не найдены TELEGRAM_BOT_TOKEN или TELEGRAM_CHAT_ID")
    sys.exit(1)

URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
PAYLOAD = {
    "chat_id": CHAT_ID,
    "text": "<b>JAA Bot Test</b>\n\nЕсли вы видите это сообщение, интеграция Telegram работает корректно! ",
    "parse_mode": "HTML"
}

print(f"Тестируем отправку в чат: {CHAT_ID}")
print("Отправка через прокси 127.0.0.1:10809...")

try:
    response = requests.post(URL, json=PAYLOAD, timeout=15, proxies=PROXIES)
    response.raise_for_status()
    result = response.json()

    if result.get("ok"):
        print("Успех! Сообщение доставлено.")
        print(f"Chat ID: {CHAT_ID}")
    else:
        print(f"Telegram API вернул ошибку: {result.get('description')}")

except requests.exceptions.ProxyError:
    print("Ошибка прокси: Не удалось подключиться к 127.0.0.1:10809")
except requests.exceptions.ConnectionError as e:
    print(f" Ошибка сети: {e}")
except Exception as e:
    print(f"Неожиданная ошибка: {e}")