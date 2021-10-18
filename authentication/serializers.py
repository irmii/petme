
from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    """ Сериализация регистрации пользователя и создания нового. """

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'token']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return {
            'email': user.email,
        }


class LoginUserSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):

        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'Введите email.'
            )

        if password is None:
            raise serializers.ValidationError(
                'Введите пароль.'
            )

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'Пользователь с введенными данным не найден.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'Данный пользователь не активен.'
            )

        if not user.is_email_verified:
            raise serializers.ValidationError(
                'Подтвердите email, пожалуйста.'
            )

        return {
            'email': user.email,
            'token': user.token
        }


class СonfirmEmailSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    code = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
