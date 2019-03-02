from django.contrib import admin
from .models import ContributionCategory, Contribution


class ContributionCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'category_for',
                    'slug', 'created_at', 'updated_at']

    class Meta:
        model = ContributionCategory


class ContributionAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'file', 'category',
                    'slug', 'is_commented', 'is_selected', 'created_at', 'updated_at']

    class Meta:
        model = Contribution


admin.site.register(ContributionCategory, ContributionCategoryAdmin)
admin.site.register(Contribution, ContributionAdmin)


