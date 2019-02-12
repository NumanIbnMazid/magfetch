from magfetch.settings.common import *
import django_heroku

DEBUG = False
TEMPLATE_DEBUG = DEBUG
SECRET_KEY = os.environ.get('SECRET_KEY')
# SECRET_KEY = 'qrd526_f3-yqr6)lf+zp6onky2oj$@6el!ua4fa2f3a(+ij$$@'
ALLOWED_HOSTS = ['magfetch.herokuapp.com', '.magfetch.com']
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_PASSWORD = 'whdmbmmnrwqxuiww'
EMAIL_HOST_USER = 'numanworkstation@gmail.com'
EMAIL_USE_TLS = True

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