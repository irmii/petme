from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.apps import apps

from authentication.serializers import (
    RegistrationSerializer,
    LoginUserSerializer,
)
from authentication.renderers import UserJSONRenderer
from authentication.tasks import send_email_confirmation
from authentication.models import User


class UserViewSet(ModelViewSet):
    """ Разрешить всем пользователям (аутентифицированным и нет) доступ к данному эндпоинту. """

    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)

    def create(self, request, *args, **kwargs):
        """Регистрация пользователя.

        Arguments:
            request: Объект запроса

        Returns:
            объект Response
        """
        user_data = request.data
        serializer = self.get_serializer_class()(data=user_data)
        if User.objects.filter(
                email=request.data.get('email'),
                is_email_verified=False,
        ).exists():
            email = request.data.get('email')
            send_email_confirmation.delay(email)
            response = Response({'email': email}, status=status.HTTP_200_OK)
        else:
            if serializer.is_valid():
                serializer.save()
                send_email_confirmation.delay(serializer.data.get('email'))
                response = Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return response

    def get_serializer_class(self):
        if self.action_map.get('post', None) == 'login':
            return LoginUserSerializer
        return RegistrationSerializer

    @action(detail=False, methods=['post'])
    def confirm_email(self, request):
        """Подтверждение email через код, высланный на почту.

        Arguments:
            request: Объект запроса

        Returns:
            объект Response
        """
        user_model = apps.get_model('authentication', 'User')
        email = request.data.get('email', None)
        code = request.data.get('code', None)
        if email and code:
            if user_model.objects.filter(
                    email=email,
                    is_email_verified=False,
            ).exists():
                user = user_model.objects.get(email=email)
                if user.get_last_confirmation_code == code:
                    user.is_email_verified = True
                    user.save()
                    response = Response(
                        {
                            'message': 'Email подтвержден!',
                            'token': user.token,
                        },
                        status=status.HTTP_200_OK
                    )
                else:
                    response = Response({'message': 'Неправильный код!'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                response = Response({'message': 'Подходящего пользователя не существует!'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            response = Response({'message': 'Недостаточно данных!'}, status=status.HTTP_400_BAD_REQUEST)
        return response

    @action(detail=False, methods=['post'])
    def send_confirm_code_again(self, request):
        """Выслать код с подтверждением еще раз.

        Arguments:
            request: Объект запроса

        Returns:
            объект Response
        """
        email = request.data.get('email', None)
        response = Response({'message': 'Введите email!'}, status=status.HTTP_400_BAD_REQUEST)
        if email:
            send_email_confirmation.delay(email)
            response = Response({'message': 'Код выслан повторно!'}, status=status.HTTP_200_OK)
        return response

    @action(detail=False, methods=['post'])
    def login(self, request):
        user_data = request.data
        serializer = self.get_serializer_class()(data=user_data)
        if serializer.is_valid():
            response = Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return response
