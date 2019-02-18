from django.shortcuts import render
# Model Import
from .models import Announcement
from accounts.models import UserProfile
# Generic View imports
from django.views.generic import DetailView
# Method Decorator imports
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Other imports


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

    # def get_context_data(self, **kwargs):
    #     context = super(AnnouncementDetailView,self).get_context_data(**kwargs)
    #     user = self.request.user
    #     profile = UserProfile.objects.filter(user=user).first()
    #     if profile.role == 4:
    #         context['base_template'] = 'landing-base.html'
    #     else:
    #         context['base_template'] = 'base.html'
    #     return context
