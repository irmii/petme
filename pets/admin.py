from django.contrib import admin

from pets.models import (
    Pet,
    Color,
    Breed,
    TypeOfPet,
)
from common.utils import all_fields_names


@admin.register(TypeOfPet)
class TypeOfPetAdmin(admin.ModelAdmin):
    """Админка TypeOfPet."""

    list_display = all_fields_names(TypeOfPet)


@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    """Админка Breed."""

    list_display = all_fields_names(Breed)


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    """Админка Color."""

    list_display = all_fields_names(Color)


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    """Админка Pet."""

    list_display = all_fields_names(Pet)
