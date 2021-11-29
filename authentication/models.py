
import jwt
from datetime import datetime, timedelta

from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models
from common.const import MAXLENGTH4


class UserManager(BaseUserManager):
    """
    Django требует, чтобы кастомные пользователи определяли свой собственный
    класс Manager.
    """

    def create_user(self, email, password=None):
        """ Создает и возвращает пользователя с имэйлом, паролем и именем. """

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        print('Тут все классно!')
        user.save()

        return user

    def create_superuser(self, username, email, password):
        """ Создает и возввращет пользователя с привилегиями суперадмина. """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Кастомная модель пользователя. """

    USERNAME_FIELD = 'email'

    username = models.CharField(max_length=255)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __str__(self):
        """ Строковое представление модели. """

        return self.email

    def get_serialized_data(self):
        return {
            'username': self.username,
            'email': self.email,
            'conf_code': self.get_last_confirmation_code,
        }

    @property
    def token(self):
        """ Позволяет получить токен пользователя путем вызова user.token. """

        return self._generate_jwt_token()

    def get_full_name(self):
        """ Будем возвращать username. """

        return self.username

    def get_short_name(self):
        """ Аналогично методу get_full_name(). """

        return self.username

    def _generate_jwt_token(self):
        """
        Генерирует веб-токен JSON, в котором хранится идентификатор этого
        пользователя, срок действия токена составляет 1 день от создания
        """
        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.encode().decode('utf-8')

    @property
    def get_last_confirmation_code(self):
        return self.user_confirmation_codes.order_by('-created').first().code


class ConfirmationCodes(models.Model):
    """Информация о высланных кодах подтверждения email."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_confirmation_codes',
    )
    code = models.CharField(
        'Код подтверждения',
        max_length=MAXLENGTH4,
    )
    created = models.DateTimeField(
        'Дата и время генерации кода',
    )

    def save(self, *args, **kwargs):
        """ Сохраняет время генерации записи. """

        if not self.id:
            self.created = timezone.now()
        return super(ConfirmationCodes, self).save(*args, **kwargs)
