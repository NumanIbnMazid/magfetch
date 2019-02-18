from django.contrib import admin
from .models import DocumentCategory, Document, Image


class DocumentCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'created_at', 'updated_at']

    class Meta:
        model = DocumentCategory


class DocumentAdmin(admin.ModelAdmin):
    list_display = ['user', 'category', 'document', 'slug', 'created_at', 'updated_at']

    class Meta:
        model = Document


class ImageAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'image', 'slug', 'created_at', 'updated_at']

    class Meta:
        model = Image


admin.site.register(DocumentCategory, DocumentCategoryAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Image, ImageAdmin)

