
import os

from django.core.wsgi import get_wsgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'magfetch.settings.development')
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'magfetch.settings.production')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'magfetch.settings.pythonanywhere')

application = get_wsgi_application()
