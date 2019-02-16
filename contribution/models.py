from django.db import models
from system_data.models import Date
from django.db.models.signals import post_save, pre_save
from accounts.utils import unique_slug_generator
from django.dispatch import receiver


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


@receiver(post_save, sender=Date)
def create_or_update_document_category(sender, instance, created, **kwargs):
    if created:
        title = 'Others'
        slug = 'others-document'
        category_filter = DocumentCategory.objects.filter(slug=slug)
        if not category_filter.exists():
            DocumentCategory.objects.create(title=title, slug=slug)


def document_category_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(document_category_pre_save_receiver, sender=DocumentCategory)
