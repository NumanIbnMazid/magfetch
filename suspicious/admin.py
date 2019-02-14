from django.contrib import admin
from .models import Suspicious

class SuspiciousAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'attempt', 'first_attempt', 'last_attempt']
    class Meta:
        model = Suspicious

admin.site.register(Suspicious, SuspiciousAdmin)
