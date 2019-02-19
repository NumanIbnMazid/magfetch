from django.db import models
from system_data.models import Date
from django.db.models.signals import post_save, pre_save
from accounts.utils import unique_slug_generator
from .utils import upload_image_path, upload_document_path, slug_generator
from accounts.models import UserProfile
from django.dispatch import receiver
import os


class DocumentCategory(models.Model):
    title = models.CharField(max_length=23, verbose_name='title')
    slug = models.SlugField(unique=True, verbose_name='slug')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')

    class Meta:
        verbose_name = 'Document Category'
        verbose_name_plural = 'Document Categories'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Document(models.Model):
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='document_user', verbose_name='user'
    )
    category = models.ForeignKey(
        DocumentCategory, related_name='document_category', null=True, blank=True, on_delete=models.CASCADE, verbose_name='category'
    )
    document = models.FileField(upload_to=upload_document_path, max_length=100)
    slug = models.SlugField(unique=True, verbose_name='slug')
    is_selected = models.BooleanField(default=False, verbose_name='is selected')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')

    class Meta:
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'
        ordering = ['-updated_at']

    def __str__(self):
        name = os.path.splitext(self.document.name)[0]
        return name


class Image(models.Model):
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='image_user', verbose_name='user'
    )
    title = models.CharField(max_length=30, verbose_name='title')
    image = models.ImageField(upload_to=upload_image_path, max_length=100)
    slug = models.SlugField(unique=True, verbose_name='slug')
    is_selected = models.BooleanField(default=False, verbose_name='is selected')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'
        ordering = ['-updated_at']

    def __str__(self):
        return self.title

@receiver(post_save, sender=Date)
def create_or_update_document_category(sender, instance, created, **kwargs):
    if created:
        title = 'Others'
        slug = 'others-document'
        category_filter = DocumentCategory.objects.filter(slug=slug)
        if not category_filter.exists():
            DocumentCategory.objects.create(title=title, slug=slug)


def document_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slug_generator(instance)
pre_save.connect(document_pre_save_receiver, sender=Document)


def image_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
pre_save.connect(image_pre_save_receiver, sender=Image)


def document_category_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
pre_save.connect(document_category_pre_save_receiver, sender=DocumentCategory)
