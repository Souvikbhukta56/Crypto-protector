from pathlib import Path
import os 

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-=tv9i#&khbv@eo(b0a0_pq!1h(=s9(ly#rj!bqwcmv0et(&pnd'
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'CryptoProtector'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'CryptoProtector.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'CryptoProtector.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3'
    }
}
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = '/static/'

# Jsonbin.io configuration
JSONBIN_API_ENDPOINT = 'https://api.jsonbin.io/v3/b'  # API endpoint
JSONBIN_API_KEY = '$2a$10$H/aJYEbeL7ZFXUyC5.j65esEHJFRfdp3U0VpjrPQeuTMpeWWBmbBC'  # Your JSON Bin API master key
