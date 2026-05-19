from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

name_validator = RegexValidator(
    regex=r'^[A-ZА-ЯЁ][a-zа-яё-]{1,}$',
    message=_('Имя/Фамилия должны начинаться с заглавной буквы, содержать минимум 2 символа. Допускается дефис.')
)


class CustomUser(AbstractUser):
    city = models.CharField(_('Город'), max_length=100)

    first_name = models.CharField(_('Имя'), max_length=150, validators=[name_validator])
    last_name = models.CharField(_('Фамилия'), max_length=150, validators=[name_validator])

    def __str__(self):
        return self.username