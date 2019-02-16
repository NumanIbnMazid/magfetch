from django.contrib import admin
from .models import DocumentCategory


class DocumentCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'created_at', 'updated_at']

    class Meta:
        model = DocumentCategory


admin.site.register(DocumentCategory, DocumentCategoryAdmin)

