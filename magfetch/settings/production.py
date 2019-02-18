from magfetch.settings.common import *
import django_heroku

SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = False
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = ['magfetch.herokuapp.com', '.magfetch.com']
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
DEBUG_COLLECTSTATIC = os.environ.get('DEBUG_COLLECTSTATIC')  # SET to 1
DISABLE_COLLECTSTATIC = os.environ.get('DISABLE_COLLECTSTATIC')  # SET to 1

ADMINS = (
    ('admin', 'admin@magfetch.com'),
)
MANAGERS = ADMINS

COMPRESS_ENABLED = os.environ.get('COMPRESS_ENABLED', False)
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
