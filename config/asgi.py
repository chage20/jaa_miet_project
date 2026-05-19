import os
import django

# 🔑 1. Сначала настраиваем Django и загружаем настройки
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

#  2. Только потом импортируем Django и Channels
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.sessions import SessionMiddlewareStack
import cars.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": SessionMiddlewareStack(
        AuthMiddlewareStack(
            URLRouter(
                cars.routing.websocket_urlpatterns
            )
        )
    ),
})