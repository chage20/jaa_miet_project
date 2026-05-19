from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import CustomUser
from .telegram_bot import send_registration_notification


@receiver(post_save, sender=CustomUser)
def notify_telegram_on_registration(sender, instance, created, **kwargs):
    """Срабатывает автоматически при создании нового пользователя."""
    if created and settings.TELEGRAM_BOT_TOKEN and settings.TELEGRAM_CHAT_ID:
        send_registration_notification(instance)
