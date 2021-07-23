from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

from common.const import MAXLENGTH15, MAXLENGTH50, MAXLENGTH200


class TypeOfPet(models.Model):
    """Тип животного."""

    type = models.CharField(
        'Тип животного, например: Кошка, Собака, Птица',
        max_length=MAXLENGTH50,
    )

    class Meta(object):
        verbose_name = 'Тип животного'
        verbose_name_plural = 'Типы животных'

    def __str__(self):
        """Строковое представление объекта.

        Returns:
            str: type
        """
        return self.type


class Color(models.Model):
    """Тип окраса."""

    name = models.CharField(
        'Тип окраса, например: Серый, Черный, Пятнистый',
        max_length=MAXLENGTH50,
    )

    class Meta(object):
        verbose_name = 'Окрас животного'
        verbose_name_plural = 'Окрасы животных'

    def __str__(self):
        """Строковое представление объекта.

        Returns:
            str: name
        """
        return self.name


class Breed(models.Model):
    """Порода."""

    name = models.CharField(
        'Название породы',
        max_length=MAXLENGTH200,
    )
    type = models.ForeignKey(
        TypeOfPet,
        related_name='type_breeds',
        on_delete=models.CASCADE,
    )

    class Meta(object):
        verbose_name = 'Порода животного'
        verbose_name_plural = 'Породы животных'

    def __str__(self):
        """Строковое представление объекта.

        Returns:
            str: name
        """
        return self.name


class Pet(models.Model):
    """Модель питомца."""

    SEX = (
        ('male', 'm'),
        ('female', 'f'),
    )

    moniker = models.CharField(
        'Кличка животного',
        max_length=MAXLENGTH200,
    )
    photo = models.ImageField('Фотография животного')
    sex = models.CharField(
        'Пол питомца',
        choices=SEX,
        max_length=MAXLENGTH15,
    )
    breed = models.ForeignKey(
        Breed,
        related_name='pets_breed',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    color = models.ForeignKey(
        Color,
        related_name='pets_color',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    birth_date = models.DateField(
        'Дата рождения',
        blank=True,
        null=True,
    )

    class Meta(object):
        verbose_name = 'Питомец'
        verbose_name_plural = 'Питомцы'

    def __str__(self):
        """Строковое представление объекта.

        Returns:
            str: moniker
        """
        return self.moniker


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    first_name = models.TextField(max_length=MAXLENGTH200)
    second_name = models.TextField(max_length=MAXLENGTH200)
    third_name = models.TextField(max_length=MAXLENGTH200)
    location = models.CharField(max_length=MAXLENGTH200)
    birth_date = models.DateField(
        null=True,
        blank=True,
    )
    phone_number = PhoneNumberField(blank=True)
    email = models.EmailField(max_length=MAXLENGTH200)

    class Meta(object):
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        """Строковое представление объекта.

        Returns:
            str: username
        """
        return self.user.username


class Attachment(models.Model):
    """Привязка человека к питомцу."""

    user = models.ForeignKey(
        Profile,
        related_name='user_pets',
        on_delete=models.CASCADE,
    )
    pet = models.ForeignKey(
        Pet,
        related_name='pet_users',
        on_delete=models.CASCADE,
    )

    class Meta(object):
        verbose_name = 'Принадлежность питомцев и пользователей'
        verbose_name_plural = 'Принадлежность питомцев и пользователей'

    def __str__(self):
        """Строковое представление объекта.

        Returns:
            str: username
        """
        return self.user + ' ' + self.pet
