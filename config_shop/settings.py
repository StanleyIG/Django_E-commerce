"""
Django settings for config_shop project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path
from dotenv import load_dotenv
import configparser

load_dotenv()

config = configparser.ConfigParser()
config.read('.env')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-p=!*etu(koo!2vs(^4cs-u2_pun6hn$1y#sh!lxdlne6za23%='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '[::1]'] #['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_bootstrap5',
    "crispy_forms",
    "crispy_bootstrap5",
    'social_django',
    'authapp_custom',
    # 'authapp',
    'mainapp',
    'basketapp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'mainapp.middleware.ExceptionMiddleware',
]

ROOT_URLCONF = 'config_shop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                 "django.template.context_processors.media", # для проброса шаблонного тэга {{ MEDIA }} -> путь к медиафайлам
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'config_shop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ.get('POSTGRES_DB'),
        "USER": os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        "HOST": "localhost",
        'PORT': '5432',
        # 'ATOMIC_REQUESTS': True,
    }
}


# Кэш

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}


# хранить данные сессии в кэшэ, увеличит производительность, если данные сессий не критически важны для данного сервиса.
SESSION_ENGINE =  "django.contrib.sessions.backends.cache"
# SESSION_CACHE_ALIAS = "default" # По умолчанию значение default, но если добавить ещё другой кэш, то нужно указать какой именно.

# celery
CELERY_BROKER_URL = "redis://127.0.0.1:6379"
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379"
CELERY_WORKER_CONCURRENCY = 4



# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

# кастомная модель пользователя
AUTH_USER_MODEL = "authapp_custom.CustomUser"


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Media файлы
# MEDIA_URL = '/media/'

# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"

JSON_PATH = 'json'

LOGIN_URL = '/auth/'
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Бэкэнды аутентификации

AUTHENTICATION_BACKENDS = [
    'social_core.backends.vk.VKOAuth2',
    "authapp_custom.authenticate.EmailAuthBackend",
    #'authapp.backends.EmailBackend',
    "social_core.backends.github.GithubOAuth2",
    'django.contrib.auth.backends.ModelBackend',
]

# куда меня редиректнет после аутентификации

LOGIN_REDIRECT_URL = "mainapp:index"
LOGOUT_REDIRECT_URL = "mainapp:index"

# Django bootstrap 5

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# разрешит использовать для хранения данных поля типа JSONField;

SOCIAL_AUTH_JSONFIELD_ENABLED = True

# настройки для социальной аутентификации

SOCIAL_AUTH_VK_OAUTH2_KEY = os.getenv('SOCIAL_AUTH_VK_OAUTH2_KEY')
SOCIAL_AUTH_VK_OAUTH2_SECRET = os.getenv('SOCIAL_AUTH_VK_OAUTH2_SECRET')


# Отправка почты

# Настроечный параметр EMAIL_BACKEND указывает класс, который будет использоваться для отправки электронной почты.
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# Email as files for debug
# EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
# EMAIL_FILE_PATH = "var/email-messages/"

# Конфигурация сервера электронной почты
# EMAIL_HOST = os.getenv('SMTP_HOST')
# EMAIL_HOST_USER = os.getenv('SMTP_USER')
# EMAIL_HOST_PASSWORD = os.getenv('SMTP_PASS')
EMAIL_HOST = config.get('smtp', 'SMTP_HOST')
EMAIL_HOST_USER = config.get('smtp', 'SMTP_USER')
EMAIL_HOST_PASSWORD = config.get('smtp', 'SMTP_PASS')
EMAIL_PORT = 465#os.getenv('SMTP_PORT')
# EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER
EMAIL_ADMIN = EMAIL_HOST_USER
