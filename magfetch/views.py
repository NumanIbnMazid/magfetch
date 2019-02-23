from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from accounts.models import UserProfile
from contribution.models import Document, Image
import datetime

# @method_decorator(login_required, name='dispatch')
# class HomeView(TemplateView):
#     template_name = 'pages/home.html'


@method_decorator(login_required, name='dispatch')
class HomeView(TemplateView):
    def get(self, request, *args, **kwargs):
        user = request.user
        user_profile_filter = UserProfile.objects.filter(user=user)
        if user_profile_filter.exists():
            profile = user_profile_filter.first()
            if profile.role == 0 or profile.role == 1 or profile.role == 2 or profile.role == 3:
                return render(request, "pages/home.html")
            if profile.role == 4:
                today = datetime.datetime.now()
                submitted_document_filter = Document.objects.filter(
                    user=profile, updated_at__year=today.year)
                if submitted_document_filter.exists():
                    submitted_document = True
                else:
                    submitted_document = False
                submitted_image_filter = Image.objects.filter(
                    user=profile, updated_at__year=today.year)
                if submitted_image_filter.exists():
                    submitted_image = True
                else:
                    submitted_image = False
                context = {
                    'submitted_document': submitted_document,
                    'submitted_image': submitted_image,
                }
                return render(request, "landing/pages/home.html", context=context)
            if profile.user.is_staff == True:
                return render(request, "pages/home.html")
            if profile.role == 7:
                return render(request, "anonymous.html")
        return render(request, "anonymous.html")
