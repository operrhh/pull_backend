import os
from .base import *
from decouple import config
from cx_Oracle import makedsn

# prueba SECURITY WARNING: don't run with debug turned on in production!
# Debug no puede ser True en produccion
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

ENGINE = 'django.db.backends.oracle'

# Leer variables de entorno
oracle_host = config('DB_DEFAULT_HOST')
oracle_port = config('DB_DEFAULT_PORT')
oracle_service_name = config('DB_DEFAULT_NAME')
oracle_user = config('DB_DEFAULT_USER')
oracle_password = config('DB_DEFAULT_PASSWORD')

# Construir la cadena DSN
dsn = makedsn(oracle_host, oracle_port, service_name=oracle_service_name)

DATABASES = {
    'default': {
        'ENGINE': ENGINE,
        'NAME': dsn,
        'USER': oracle_user,
        'PASSWORD': oracle_password,
    },
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
