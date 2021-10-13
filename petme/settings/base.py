"""Base settings."""
import os
from decouple import config
import dj_database_url


# Build paths inside the project like this: BASE_DIR / 'subdir'.
SETTINGS_DIR = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(os.path.dirname(SETTINGS_DIR))
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=False, cast=bool)

SECRET_KEY = config("SECRET_KEY", default='hello')

ALLOWED_HOSTS = [
    'petme.petme.company',
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'pets',
    'phonenumber_field',
    'common',
    'authentication',
    'django_extensions',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'django_celery_results',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'petme.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'petme.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {'default': dj_database_url.config(conn_max_age=600, ssl_require=True)}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# manage.py createdefaultsuperuser (command)
TEST_DEFAULT_ADMIN_USERNAME = config('TEST_DEFAULT_ADMIN_USERNAME', default='admin')
TEST_DEFAULT_ADMIN_PASSWORD = config('TEST_DEFAULT_ADMIN_PASSWORD', default='superuser')
TEST_DEFAULT_ADMIN_EMAIL = config('TEST_DEFAULT_ADMIN_PASSWORD', default='zazzzu@yandex.ru')


# Использовать кастомную модель
AUTH_USER_MODEL = 'authentication.User'


# django-allauth settings
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 2

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'ru-RU'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'petme.exceptions.core_exception_handler',
    'NON_FIELD_ERRORS_KEY': 'error',
}

# Настройки SMTP
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
MAILER_EMAIL_BACKEND = EMAIL_BACKEND
EMAIL_HOST = config('EMAIL_HOST', default='your_mail_server')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='your_password')
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='your_email')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_USE_SSL = config("EMAIL_USE_SSL", default=True, cast=bool)
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# Celery
CELERY_BROKER_URL = config('CELERY_BROKER_URL', default="amqp://rabbitmquser:some_password@rabbitmq:5672")
CELERY_RESULT_BACKEND = 'django-db'
CELERY_TIMEZONE = 'Europe/Moscow'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
