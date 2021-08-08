
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from authentication.viewsets import UserViewSet


app_name = 'authentication'

router = DefaultRouter()

router.register(
    'users',
    UserViewSet,
    basename='registration_user',
)

urlpatterns = [
    path('', include(router.urls)),
]
