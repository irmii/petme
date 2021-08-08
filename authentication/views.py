
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.serializers import RegistrationSerializer, LoginUserSerializer
from authentication.renderers import UserJSONRenderer
from authentication.tasks import send_email_confirmation


class RegistrationAPIView(APIView):
    """ Разрешить всем пользователям (аутентифицированным и нет) доступ к данному эндпоинту. """

    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        send_email_confirmation.delay(serializer.data.get('email'))

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    """ Разрешить всем пользователям (аутентифицированным и нет) доступ к данному эндпоинту. """

    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginUserSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
