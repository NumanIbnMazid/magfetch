from django.urls import path
from .views import AnnouncementDetailView

urlpatterns = [
    path('announcement/<slug>/detail/', AnnouncementDetailView.as_view(), name='announcement_detail'),
]
