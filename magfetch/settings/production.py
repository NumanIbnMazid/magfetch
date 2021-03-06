from magfetch.settings.common import *
import django_heroku

SECRET_KEY = os.environ.get('SECRET_KEY')
# SECRET_KEY = 'qrd526_f3-yqr6)lf+zp6onky2oj$@6el!ua4fa2f3a(+ij$$@'
# DEBUG = True
DEBUG = os.environ.get('DEBUG')
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = ['magfetch.pythonanywhere.com',
                 'magfetch.herokuapp.com', '.magfetch.com']
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
# DEBUG_COLLECTSTATIC = os.environ.get('DEBUG_COLLECTSTATIC')  # SET to 1
# DISABLE_COLLECTSTATIC = os.environ.get('DISABLE_COLLECTSTATIC')  # SET to 1

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

ADMINS = (
    ('admin', 'admin@magfetch.com'),
)
MANAGERS = ADMINS

# Static Files
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static_proj'),
]
STATIC_ROOT = os.path.join('static_cdn', 'static_root')
MEDIA_ROOT = os.path.join('static_cdn', 'media_root')

# HEROKU DEPLOYMENT

CORS_REPLACE_HTTPS_REFERER      = True
HOST_SCHEME                     = "https://"
SECURE_PROXY_SSL_HEADER         = ('HTTP_X_FORWARDER_PROTO', 'https')
SECURE_SSL_REDIRECT             = True
SESSION_COOKIE_SECURE           = True
CSRF_COOKIE_SECURE              = True
SECURE_HSTS_INCLUDE_SUBDOMAINS  = True
SECURE_HSTS_SECONDS             = 1000000
SECURE_FRAME_DENY               = True

# HEROKU DEPLOYMENT

# Activate Django-Heroku.
django_heroku.settings(locals())

