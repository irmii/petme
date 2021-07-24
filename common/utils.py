"""Модуль утилит."""


def all_fields(model):
    return [field for field in model._meta.fields]


def all_fields_names(model):
    return [field.name for field in all_fields(model)]
