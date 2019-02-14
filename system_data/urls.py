from django.urls import path
from .views import DateCreateView

urlpatterns = [
    path('schedule/create/', DateCreateView.as_view(), name='date_create'),
]
