from django.contrib import admin
from .models import Announcement

class AnnouncementAdmin(admin.ModelAdmin):
    list_display    = ['created_by', 'slug', 'category', 'identifier', 'subject', 'status', 'created_at', 'updated_at']
    class Meta:
        model       = Announcement

admin.site.register(Announcement, AnnouncementAdmin)
