import os
from .base import *
from decouple import config
from cx_Oracle import makedsn

# prueba SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['192.168.0.107','0.0.0.0','127.0.0.1','localhost','web', '168.138.71.27', '129.151.110.152']

# Database conex
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

ENGINE = 'django.db.backends.oracle'


# Leer variables de entorno
OCI_HOST = config('DB_DEFAULT_HOST')
OCI_PORT = config('DB_DEFAULT_PORT')
OCI_SERVICE_NAME = config('DB_DEFAULT_NAME')
OCI_USER = config('DB_DEFAULT_USER')
OCI_PASSWORD = config('DB_DEFAULT_PASSWORD')

PEOPLE_HOST = config('DB_PEOPLE_SOFT_HOST')
PEOPLE_PORT = config('DB_PEOPLE_SOFT_PORT')
PEOPLE_SERVICE_NAME = config('DB_PEOPLE_SOFT_NAME')
PEOPLE_USER = config('DB_PEOPLE_SOFT_USER')
PEOPLE_PASSWORD = config('DB_PEOPLE_SOFT_PASSWORD')

OCI_DSN = makedsn(OCI_HOST, OCI_PORT, service_name=OCI_SERVICE_NAME)
PEOPLE_DSN = makedsn(PEOPLE_HOST, PEOPLE_PORT, service_name=PEOPLE_SERVICE_NAME)


DATABASES = {
    'default': {
        'ENGINE': ENGINE,
        'NAME': OCI_DSN,
        'USER': OCI_USER,
        'PASSWORD': OCI_PASSWORD,
    },
   'people_soft': {
       'ENGINE': ENGINE,
       'NAME': PEOPLE_DSN,
       'USER': PEOPLE_USER,
       'PASSWORD': PEOPLE_PASSWORD,
   }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
