from django.db import models
from system_data.models import Date
from django.db.models.signals import post_save, pre_save
from accounts.utils import unique_slug_generator
from .utils import upload_contribution_path
from accounts.models import UserProfile
from django.dispatch import receiver
import os



class ContributionCategory(models.Model):
    DOCUMENT = 0
    IMAGE = 1
    CONTRIBUTION_CATEGORY_CHOICES = (
        (DOCUMENT, 'Documents'),
        (IMAGE, 'Images')
    )
    category_for = models.PositiveSmallIntegerField(
        choices=CONTRIBUTION_CATEGORY_CHOICES, default=0, verbose_name=('category for')
    )
    title = models.CharField(max_length=23, verbose_name='title')
    slug = models.SlugField(unique=True, verbose_name='slug')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')

    class Meta:
        verbose_name = 'Contribution Category'
        verbose_name_plural = 'Contribution Categories'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Contribution(models.Model):
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='user_contribution', verbose_name='user'
    )
    title = models.CharField(max_length=30, verbose_name='title')
    file = models.FileField(
        upload_to=upload_contribution_path, max_length=100, verbose_name='file')
    category = models.ForeignKey(
        ContributionCategory, related_name='contribution_category', on_delete=models.CASCADE, verbose_name='category'
    )
    slug = models.SlugField(unique=True, verbose_name='slug')
    is_commented = models.BooleanField(default=False, verbose_name='is commented')
    is_selected = models.BooleanField(default=False, verbose_name='is selected')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')

    class Meta:
        verbose_name = 'Contribution'
        verbose_name_plural = 'Contributions'
        ordering = ['-updated_at']

    def __str__(self):
        return self.title


@receiver(post_save, sender=Date)
def create_or_update_contribution_category(sender, instance, created, **kwargs):
    if created:
        document_slug = 'other-document'
        image_slug = 'other-image'
        doc_category_filter = ContributionCategory.objects.filter(
            slug=document_slug, category_for=0)
        img_category_filter = ContributionCategory.objects.filter(
            slug=image_slug, category_for=1)
        if not doc_category_filter.exists():
            document_title = 'Other Document'
            ContributionCategory.objects.create(
                title=document_title, slug=document_slug, category_for=0)
        if not img_category_filter.exists():
            image_title = 'Other Image'
            ContributionCategory.objects.create(
                title=image_title, slug=image_slug, category_for=1)


def contribution_category_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(contribution_category_pre_save_receiver, sender=ContributionCategory)


