from .base import *
from decouple import config


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

ENGINE = 'django.db.backends.oracle'

DATABASES = {
    'default': {
        'ENGINE': ENGINE,
        'NAME': config('DB_DEFAULT_NAME'),
        'USER': config('DB_DEFAULT_USER'),
        'PASSWORD': config('DB_DEFAULT_PASSWORD'),
        'HOST': config('DB_DEFAULT_HOST'),
        'PORT': config('DB_DEFAULT_PORT')
    },
    # 'people_soft_luky': {
    #     'ENGINE': ENGINE,
    #     'NAME': config('DB_PEOPLE_SOFT_LUKY_NAME'),
    #     'USER': config('DB_PEOPLE_SOFT_LUKY_USER'),
    #     'PASSWORD': config('DB_PEOPLE_SOFT_LUKY_PASSWORD'),
    #     'HOST': config('DB_PEOPLE_SOFT_LUKY_HOST'),
    #     'PORT': config('DB_PEOPLE_SOFT_LUKY_PORT')
    # },
    'people_soft': {
        'ENGINE': ENGINE,
        'NAME': config('DB_PEOPLE_SOFT_NAME'),
        'USER': config('DB_PEOPLE_SOFT_USER'),
        'PASSWORD': config('DB_PEOPLE_SOFT_PASSWORD'),
        'HOST': config('DB_PEOPLE_SOFT_HOST'),
        'PORT': config('DB_PEOPLE_SOFT_PORT')
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'