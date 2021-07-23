"""Модуль создания супер пользователя по умолчанию."""

from django.conf import settings
from authentication.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Клссс консольной команды."""

    help = 'Создаёт суперпользователя по умолчанию'  # noqa

    def handle(self, *args, **options):  # noqa
        """Выполняет консольную команду.

        Arguments:
            args: Аргументы
            options: Переданные параметры команды
        """
        username = settings.TEST_DEFAULT_ADMIN_USERNAME
        password = settings.TEST_DEFAULT_ADMIN_PASSWORD
        email = settings.TEST_DEFAULT_ADMIN_EMAIL
        default_superuser = User.objects.filter(username=username).first()
        if not default_superuser:
            User.objects.create_superuser(username=username, password=password, email=email)  # type: ignore
