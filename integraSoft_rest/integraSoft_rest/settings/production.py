import os
from .base import *
from decouple import config
from cx_Oracle import makedsn

# prueba SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["192.168.0.107", "127.0.0.1", "0.0.0.0", "web"]

# Database conex
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

ENGINE = 'django.db.backends.oracle'


# Leer variables de entorno
oci_host = config('DB_DEFAULT_HOST')
oci_port = config('DB_DEFAULT_PORT')
oci_service_name = config('DB_DEFAULT_NAME')
oci_user = config('DB_DEFAULT_USER')
oci_password = config('DB_DEFAULT_PASSWORD')

people_host = config('DB_PEOPLE_SOFT_HOST')
people_port = config('DB_PEOPLE_SOFT_PORT')
people_service_name = config('DB_PEOPLE_SOFT_NAME')
people_user = config('DB_PEOPLE_SOFT_USER')
people_password = config('DB_PEOPLE_SOFT_PASSWORD')

oci_dsn = makedsn(oci_host, oci_port, service_name=oci_service_name)
people_dsn = makedsn(people_host, people_port, service_name=people_service_name)


DATABASES = {
    'default': {
        'ENGINE': ENGINE,
        'NAME': oci_dsn,
        'USER': oci_user,
        'PASSWORD': oci_password,
    },
#    'people_soft': {
#        'ENGINE': ENGINE,
#        'NAME': people_dsn,
#        'USER': people_user,
#        'PASSWORD': people_password,
#    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
