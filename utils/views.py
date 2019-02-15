from django.shortcuts import render
# Model Import
from .models import Announcement
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
