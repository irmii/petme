
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView
from django.urls import path, include
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('authentication.urls', namespace='authentication')),
    path('accounts/', include('allauth.urls')),
    path('', TemplateView.as_view(template_name="index.html")),
    path('accounts/', include('allauth.urls')),
    path('logout', LogoutView.as_view()),
    path(
            'openapi/',
            get_schema_view(
                title='Svetofor',
                description='API for svetofor project',
                version='1.0.0',
            ),
            name='openapi-schema',
        ),
    path(
        'swagger/',
        TemplateView.as_view(
            template_name='common/swagger-ui.html',
            extra_context={'schema_url': 'openapi-schema'},
        ),
        name='swagger-ui',
    ),
    path('api/', include('pets.urls'))
]
