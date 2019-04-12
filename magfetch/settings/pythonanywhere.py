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
        'NAME': config('DB_NAME_PAW'),
        'USER': config('DB_USER_PAW'),
        'PASSWORD': config('DB_PASSWORD_PAW'),
        'HOST': config('DB_HOST_PAW'),
        'PORT': '',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# Static Files
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static_proj'),
]
# STATIC_ROOT = os.path.join('static_cdn', 'static_root')
# MEDIA_ROOT = os.path.join('static_cdn', 'media_root')

STATIC_ROOT = /home/magfetch/static_cdn/static_root
MEDIA_ROOT = /home/magfetch/static_cdn/media_root

# Neededf for CorsHeader (accept connections from everywhere)
CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_HEADERS = (
    'x-requested-with',
    'content-type',
    'accept',
    'origin',
    'authorization',
    'x-csrftoken',
    'token',
    'x-device-id',
    'x-device-type',
    'x-push-id',
    'dataserviceversion',
    'maxdataserviceversion'
)
CORS_ALLOW_METHODS = (
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS'
)