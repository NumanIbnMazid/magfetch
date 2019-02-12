from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, Faculty

UserAdmin.list_display += ('is_active',)

class FacultyAdmin(admin.ModelAdmin):
    list_display = ['code', 'title', 'created_at', 'updated_at']
    class Meta:
        model = Faculty

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'slug', 'role', 'faculty', 'created_at', 'updated_at']
    class Meta:
        model = UserProfile

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Faculty, FacultyAdmin)
