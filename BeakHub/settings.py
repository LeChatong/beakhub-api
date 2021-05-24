"""
Django settings for BeakHub project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from decouple import config
from dj_database_url import parse as dburl
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
from corsheaders.defaults import default_headers

BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8^et=8@1g!2ah0o33^@v%$_)*c%zwfd5nf*mrh_+-j8-w=faz^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    "localhost",
    "172.16.30.38",
    "127.0.0.1",
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # Utils Apps
    'import_export',
    'rest_framework',
    'rest_framework_api_key',
    'corsheaders',
    'django_countries',
    'django_filters',
    'phonenumber_field',
    'drf_yasg',
    # Local Apps
    'Apps.core',
    'Apps.account',
    'Apps.job',
    'Apps.address',
    'Apps.comment',
    'Apps.favorite',
]

# Custom User Model
AUTH_USER_MODEL = 'account.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

SITE_ID = 1

ROOT_URLCONF = 'BeakHub.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = 'BeakHub.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

_DEFAULT_DATABASE_URL = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')

DATABASES = {'default': config(
    'DATABASE_URL', default=_DEFAULT_DATABASE_URL, cast=dburl), }

#DATABASES = {
#    'default': {
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#        'ENGINE': 'django.db.backends.postgresql',
#        'NAME': 'beakhub',
#        'USER': 'postgres',
#        'PASSWORD': '123456',
#        'HOST': '',
#        'PORT': '5433',
#    }
#}


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

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


gettext = lambda x: x

LANGUAGES = (
    ('fr', gettext('French')),
    ('en', gettext('English')),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, "Public", "media")
MEDIA_URL = "/media/"

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIR = [
    ("static", os.path.join(BASE_DIR, "Public", "static"))
]

GRAPPELLI_ADMIN_TITLE = os.environ.get("GRAPPELLI_ADMIN_TITLE", "BeakHub Admin")

DEFAULT_COUNTRY = "CM"

LOCALE_PATHS = (
    os.path.join(BASE_DIR, '/locale/'),
)

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework_api_key.permissions.HasAPIKey',
    )

}

API_KEY_CUSTOM_HEADER = "HTTP_X_API_KEY"
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = list(default_headers) + [
    'x-api-key',
]

SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': True,
    'SECURITY_DEFINITIONS': {
        'API Key': {
            "type": "apiKey",
            "name": "x-api-key",
            "in": "header"
        },
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}

#GRAPPELLI_INDEX_DASHBOARD = 'BeakHub.dashboard.CustomIndexDashboard'
#GRAPPELLI_INDEX_DASHBOARD = {  # alternative method
#    'yourproject.admin.admin_site': 'yourproject.my_dashboard.CustomIndexDashboard',
#}
