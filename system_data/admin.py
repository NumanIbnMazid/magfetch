from django.contrib import admin
from .models import Date

class DateAdmin(admin.ModelAdmin):
    list_display    = ['academic_year', 'start_date', 'closure_date', 'final_closure_date', 'created_at', 'updated_at']
    class Meta:
        model       = Date

admin.site.register(Date, DateAdmin)