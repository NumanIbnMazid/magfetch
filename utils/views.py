from django.shortcuts import render
# Model Import
from .models import Announcement, Notification
from accounts.models import UserProfile
from suspicious.models import Suspicious
# Generic View imports
from django.views.generic import DetailView, ListView
# Method Decorator imports
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Other imports
import datetime
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse


# ------------------------- Announcement Detail View ---------------------------
@method_decorator(login_required, name='dispatch')
class AnnouncementDetailView(DetailView):
    template_name   = 'announcement/announcement-detail.html'

    def get_object(self):
        slug                = self.kwargs['slug']
        announcement_filter = Announcement.objects.filter(slug=slug)
        if announcement_filter.exists():
            announcement    = announcement_filter.first()
            return announcement
        return None

    def get_context_data(self, **kwargs):
        context = super(AnnouncementDetailView,self).get_context_data(**kwargs)
        user = self.request.user
        profile = UserProfile.objects.filter(user=user).first()
        if profile.role == 4:
            context['base_template'] = 'landing-base.html'
        else:
            context['base_template'] = 'base.html'
        return context


# ------------------------- Notification List View ---------------------------
@method_decorator(login_required, name='dispatch')
class NotificationListView(ListView):
    template_name = 'notification/list.html'
    paginate_by = 4
    model = Notification
    # context_object_name = 'objects'

    def get_queryset(self, *args, **kwargs):
        request = self.request
        user_profile_filter = UserProfile.objects.filter(user=request.user)
        if user_profile_filter.exists():
            profile = user_profile_filter.first()
            query = Notification.objects.filter(
                receiver=profile).order_by('-updated_at')
        return query


# ------------------------- Notification Detail View ---------------------------
@method_decorator(login_required, name='dispatch')
class NotificationDetailView(DetailView):
    template_name = 'notification/notification-detail.html'

    def get_object(self):
        slug = self.kwargs['slug']
        notification_filter = Notification.objects.filter(slug=slug)
        if notification_filter.exists():
            notification = notification_filter.first()
            if notification.has_read == False:
                notification_filter.update(has_read=True)
            return notification
        return None

    def user_passes_test(self, request):
        user = request.user
        self.object = self.get_object()
        profile = UserProfile.objects.filter(user=user).first()
        if self.object.receiver == profile:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        instance_user = self.request.user
        if not self.user_passes_test(request):
            suspicious_user = Suspicious.objects.filter(user=instance_user)
            if suspicious_user.exists():
                suspicious_user_instance = Suspicious.objects.get(
                    user=instance_user)
                current_attempt = suspicious_user_instance.attempt
                total_attempt = current_attempt + 1
                update_time = datetime.datetime.now()
                suspicious_user.update(
                    attempt=total_attempt, last_attempt=update_time)
            else:
                Suspicious.objects.get_or_create(user=instance_user)
            messages.add_message(self.request, messages.ERROR,
                                 "You are not allowed. Your account is being tracked for suspicious activity !"
                                 )
            return HttpResponseRedirect(reverse('home'))
        return super(NotificationDetailView, self).dispatch(request, *args, **kwargs)
