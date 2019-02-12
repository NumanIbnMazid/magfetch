from django.db import models
from django.conf import settings
from .utils import time_str_mix_slug
from django.db.models.signals import post_save
from django.dispatch import receiver

class Faculty(models.Model):
    code        = models.CharField(max_length=7, unique=True, verbose_name=('code'))
    title       = models.CharField(max_length=50, verbose_name=('title'))
    created_at  = models.DateTimeField(auto_now_add=True, verbose_name=('created at'))
    updated_at  = models.DateTimeField(auto_now=True, verbose_name=('updated at'))

    class Meta:
        verbose_name        = ('Faculty')
        verbose_name_plural = ('Faculties')
        ordering            = ["-created_at"]

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    MARKETING_MANAGER       = 0
    ADMINISTRATOR           = 1
    MARKETING_COORDINATOR   = 2
    FACULTY_GUEST           = 3
    STUDENT                 = 4

    USER_ROLE_CHOICES       = (
        (MARKETING_MANAGER, 'Marketing Manager'),
        (ADMINISTRATOR, 'Administrator'),
        (MARKETING_COORDINATOR, 'Marketing Coordinator'),
        (FACULTY_GUEST, 'Faculty Guest'),
        (STUDENT, 'Student')
    )

    user        = models.OneToOneField(
        settings.AUTH_USER_MODEL, unique=True, on_delete=models.CASCADE, related_name='profile', verbose_name=('user')
    )
    slug        = models.SlugField(unique=True, max_length=255, verbose_name=('slug'))
    role   = models.PositiveSmallIntegerField(
        choices = USER_ROLE_CHOICES, null=True, blank=True, default=4, verbose_name=('role')
    )
    faculty     = models.ForeignKey(Faculty, null=True, blank=True, on_delete=models.CASCADE, related_name='user_faculty', verbose_name=("faculty"))
    created_at  = models.DateTimeField(auto_now_add=True, verbose_name=('created at'))
    updated_at  = models.DateTimeField(auto_now=True, verbose_name=('updated at'))

    class Meta:
        verbose_name        = ('User Profile')
        verbose_name_plural = ('User Profiles')
        ordering            = ["-user__date_joined"]

    def get_smallname(self):
        if self.user.first_name or self.user.last_name:
            name = self.user.get_short_name()
        else:
            name = self.user.username
        return name

    def get_role(self):
        if self.role == 0:
            role = "Marketing Manager"
        if self.role == 1:
            role = "Administrator"
        if self.role == 2:
            role = "Marketing Coordinator"
        if self.role == 3:
            role = "Faculty Guest"
        if self.role == 4:
            role = "Student"
        return role

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    username        = instance.username.lower()
    slug_binding    = username+'-'+time_str_mix_slug()
    if created:
        UserProfile.objects.create(user=instance, slug=slug_binding)
    instance.profile.save()