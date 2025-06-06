# url_monitor/settings.py 

from pathlib import Path
import os
import sys # Necesario para sys._MEIPASS -Fernando

# Misma función que en start_app.py para simplicidad al empaquetar -Fernando
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-test-key'
DEBUG = True 
ALLOWED_HOSTS = ['127.0.0.1', 'localhost'] # Definir esto explícitamente -Fernando

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'monitor', 
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

ROOT_URLCONF = 'url_monitor.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [resource_path('templates')],
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

WSGI_APPLICATION = 'url_monitor.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': resource_path('db.sqlite3'),
    }
}

LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'Europe/Madrid'
USE_I18N = True
USE_TZ = True


STATIC_URL = '/static/'
#nuevo codigo Alejandro 28/5/2025 se implementa codigo para quitar el WARNING O error staticfiles.W004
STATICFILES_DIRS = [BASE_DIR / 'monitor' / 'static']


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
#nuevo codigo Alejandro 19/5/2025 se implementa codigo para guardar archivo en la base de datos

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

#nuevo codigo Alejandro 19/5/2025 se implementa codigo para guardar archivo en la base de datos
