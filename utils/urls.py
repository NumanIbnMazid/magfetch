from django.urls import path
from .views import AnnouncementDetailView, NotificationDetailView, NotificationListView

urlpatterns = [
    path('announcement/<slug>/detail/', AnnouncementDetailView.as_view(), name='announcement_detail'),
    path('notification/list/', NotificationListView.as_view(), name='notification_list'),
    path('notification/<slug>/detail/', NotificationDetailView.as_view(), name='notification_detail'),
]
