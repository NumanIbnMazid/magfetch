from django.db import models
from system_data.models import Date
from django.db.models.signals import post_save, pre_save
from accounts.utils import unique_slug_generator
from .utils import upload_contribution_path
from accounts.models import UserProfile
from django.dispatch import receiver
from django.urls import reverse
from django.db.models import Q
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

    def get_file_type(self):
        if self.category_for == 0:
            return "DOCUMENT"
        if self.category_for == 1:
            return "IMAGE"
        return None


class ContributionQuerySet(models.query.QuerySet):
    def commented(self):
        return self.filter(is_commented=True)

    def uncommented(self):
        return self.filter(is_commented=False)

    def selected(self):
        return self.filter(is_selected=True)

    def latest(self):
        return self.filter().order_by('-created_at')

    def search(self, query):
        lookups = (Q(title__icontains=query) |
                   Q(category__icontains=query) |
                   Q(user__faculty__title__icontains=query) |
                   Q(user__user__username__icontains=query) |
                   Q(user__user__first_name__icontains=query) |
                   Q(user__user__last_name__icontains=query) |
                   Q(user__user__email__icontains=query)
                   )
        return self.filter(lookups).distinct()

class ContributionManager(models.Manager):
    def get_queryset(self):
        return ContributionQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def get_by_slug(self, slug):
        qs = self.get_queryset().filter(slug=slug)
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self, query):
        return self.get_queryset()


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

    objects = ContributionManager()

    class Meta:
        verbose_name = 'Contribution'
        verbose_name_plural = 'Contributions'
        ordering = ['-updated_at']

    def get_absolute_url(self):
        return reverse("contribution:contribution_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title

    def get_selection_status(self):
        if self.is_selected == True:
            return "SELECTED"
        else:
            return "NOT SELECTED"
        return None

    def get_file_extension(self):
        fileName, fileExtension = os.path.splitext(self.file.name)
        return fileExtension



class Comment(models.Model):
    contribution = models.ForeignKey(
        Contribution, on_delete=models.CASCADE, related_name='user_contribution_file', verbose_name='contribution'
    )
    commented_by = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='user_comment', verbose_name='commented by'
    )
    comment = models.TextField(max_length=1000, verbose_name='comment')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['-updated_at']

    def __str__(self):
        return self.contribution.title



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


def contribution_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(contribution_pre_save_receiver, sender=Contribution)


# @receiver(post_save, sender=Comment)
# def create_or_update_comment_status(sender, instance, created, **kwargs):
#     if created:
#         contribution_filter = Contribution.objects.filter(slug=instance.contribution.slug)
#         if contribution_filter.exists():
#             if contribution_filter.first().is_commented == False:
#                 contribution_filter.update(is_commented=True)


