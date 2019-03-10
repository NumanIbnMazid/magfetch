from magfetch.settings.common import *
from decouple import config, Csv

SECRET_KEY = config('SECRET_KEY')
DEBUG = False
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())
EMAIL_BACKEND = config('EMAIL_BACKEND', default='')
EMAIL_HOST = config('EMAIL_HOST', default='localhost')
EMAIL_PORT = config('EMAIL_PORT', default=25, cast=int)
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER_PAW'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST_PAW'),
        'PORT': '',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
