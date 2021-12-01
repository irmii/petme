from django.urls import path
from .views import BreedsAPIView

urlpatterns = [
    path('breeds/', BreedsAPIView.as_view())
]