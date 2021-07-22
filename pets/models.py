from django.db import models

from common.const import MAXLENGTH15, MAXLENGTH50, MAXLENGTH200


class TypeOfPet(models.Model):
    """Тип животного."""

    type = models.CharField(
        'Тип животного, например: Кошка, Собака, Птица',
        max_length=MAXLENGTH50,
    )


class Color(models.Model):
    """Тип окраса."""

    name = models.CharField(
        'Тип окраса, например: Серый, Черный, Пятнистый',
        max_length=MAXLENGTH50,
    )


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
