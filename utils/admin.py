from django.contrib import admin
from .models import Announcement, Notification


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['slug', 'category', 'identifier',
                    'subject', 'status', 'created_at', 'updated_at']

    class Meta:
        model = Announcement


class NotificationAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'slug', 'category', 'identifier',
                    'has_read', 'created_at', 'updated_at']

    class Meta:
        model = Notification


admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Notification, NotificationAdmin)
