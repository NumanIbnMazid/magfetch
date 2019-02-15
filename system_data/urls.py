from django.urls import path
from .views import DateCreateView, DateUpdateView

urlpatterns = [
    path('schedule/create/', DateCreateView.as_view(), name='date_create'),
    path('schedule/update/', DateUpdateView.as_view(), name='date_update'),
]
