from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('account/', include('accounts.urls')),
    path('system/data/', include(('system_data.urls', 'system_data'), namespace='system_data')),
    path('utils/', include(('utils.urls', 'utils'), namespace='utils')),
    path('contribution/', include(('contribution.urls', 'contribution'), namespace='contribution')),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
