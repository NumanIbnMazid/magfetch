from django.db import models
from accounts.models import UserProfile

class Announcement(models.Model):
    PUBLISHED       = 0
    UNPUBLISHED     = 1

    STATUS_CHOICES  = (
        (PUBLISHED, 'Published'),
        (UNPUBLISHED, 'Unpublished'),
    )

    created_by      = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='announcement_created_by', verbose_name=('created by')
    )
    category        = models.CharField(max_length=20, null=True, blank=True, verbose_name=('category'))
    slug            = models.SlugField(unique=True, verbose_name=('slug'))
    identifier      = models.CharField(max_length=200, null=True, blank=True, verbose_name=('identifier'))
    subject         = models.CharField(max_length=100, null=True, blank=True, verbose_name=('subject'))
    message         = models.TextField(max_length=500, null=True, blank=True, verbose_name=('message'))
    status              = models.PositiveSmallIntegerField(
        choices = STATUS_CHOICES, default=0, verbose_name=('status')
    )
    created_at      = models.DateTimeField(auto_now_add=True, verbose_name=('created at'))
    updated_at      = models.DateTimeField(auto_now=True, verbose_name=('updated at'))

    class Meta:
        verbose_name        = "Announcement"
        verbose_name_plural = "Announcements"
        ordering            = ["-updated_at"]

    def __str__(self):
        return self.category


class Notification(models.Model):
    sender = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='notification_sender', null=True, blank=True, verbose_name=('sender')
    )
    receiver = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='notification_receiver', null=True, blank=True, verbose_name=('receiver')
    )
    category = models.CharField(
        max_length=20, null=True, blank=True, verbose_name=('category'))
    identifier = models.CharField(
        max_length=200, null=True, blank=True, verbose_name=('identifier'))
    slug = models.SlugField(unique=True, verbose_name=('slug'))
    subject = models.TextField(
        max_length=300, null=True, blank=True, verbose_name=('subject'))
    message = models.TextField(
        max_length=500, null=True, blank=True, verbose_name=('message'))
    has_read = models.BooleanField(default=False, verbose_name=('has read'))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=('created at'))
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=('updated at'))

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ["-updated_at"]

    def __str__(self):
        return self.category
