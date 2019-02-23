from django import template
from accounts.models import UserProfile
from system_data.models import Date
from utils.models import Announcement, Notification
import datetime

register = template.Library()

@register.simple_tag(takes_context=True)
def is_MM_tag(context):
    request         = context['request']
    user            = request.user
    user_profile_filter = UserProfile.objects.filter(user=user)
    if user_profile_filter.exists():
        if user_profile_filter.first().role == 0:
            return True
    return False

@register.simple_tag(takes_context=True)
def is_AD_tag(context):
    request         = context['request']
    user            = request.user
    user_profile_filter = UserProfile.objects.filter(user=user)
    if user_profile_filter.exists():
        if user_profile_filter.first().role == 1:
            return True
    return False

@register.simple_tag(takes_context=True)
def is_MC_tag(context):
    request         = context['request']
    user            = request.user
    user_profile_filter = UserProfile.objects.filter(user=user)
    if user_profile_filter.exists():
        if user_profile_filter.first().role == 2:
            return True
    return False

@register.simple_tag(takes_context=True)
def is_FG_tag(context):
    request         = context['request']
    user            = request.user
    user_profile_filter = UserProfile.objects.filter(user=user)
    if user_profile_filter.exists():
        if user_profile_filter.first().role == 3:
            return True
    return False

@register.simple_tag(takes_context=True)
def is_ST_tag(context):
    request         = context['request']
    user            = request.user
    user_profile_filter = UserProfile.objects.filter(user=user)
    if user_profile_filter.exists():
        if user_profile_filter.first().role == 4:
            return True
    return False

@register.simple_tag(takes_context=True)
def get_schedule_tag(context):
    today           = datetime.datetime.now()
    schedule_filter = Date.objects.filter(academic_year=today.year)
    if schedule_filter.exists():
        schedule    = schedule_filter.first()
        return schedule
    return None

@register.simple_tag(takes_context=True)
def get_announcement_tag(context):
    announcement_filter = Announcement.objects.filter(status=0).order_by('-updated_at')
    if announcement_filter.count() > 0:
        return announcement_filter
    return None


@register.simple_tag(takes_context=True)
def get_notification_tag(context):
    request = context['request']
    user = request.user
    user_profile_filter = UserProfile.objects.filter(user=user)
    if user_profile_filter.exists():
        user_profile = user_profile_filter.first()
        notification_filter = Notification.objects.filter(
            receiver=user_profile).order_by('-updated_at')
        return notification_filter
    return None


@register.simple_tag(takes_context=True)
def get_notification_unread_counter_tag(context):
    request = context['request']
    user = request.user
    user_profile_filter = UserProfile.objects.filter(user=user)
    if user_profile_filter.exists():
        user_profile = user_profile_filter.first()
        notification_filter = Notification.objects.filter(
            receiver=user_profile, has_read=False).order_by('-updated_at')
        return notification_filter.count()
    return None


@register.simple_tag(takes_context=True)
def get_datetime_tag(context):
    return datetime.datetime.now()
