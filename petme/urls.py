
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('authentication.urls', namespace='authentication')),
    path('accounts/', include('allauth.urls')),
    path('', TemplateView.as_view(template_name="index.html")),
    path('accounts/', include('allauth.urls')),
    path('logout', LogoutView.as_view()),
]
