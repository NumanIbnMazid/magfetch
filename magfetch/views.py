from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from accounts.models import UserProfile
from contribution.models import Contribution
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
            # Administrative Dashboard View
            if profile.role == 0 or profile.role == 1 or profile.role == 2 or profile.role == 3:
                return render(request, "pages/home.html")
            # Student Landing Page View
            if profile.role == 4:
                today = datetime.datetime.now()

                submitted_filter = Contribution.objects.filter(
                    user=profile, updated_at__year=today.year)
                if submitted_filter.exists():
                    is_submitted = True
                else:
                    is_submitted = False

                context = {
                    'is_submitted': is_submitted
                }
                return render(request, "landing/pages/home.html", context=context)
            # Django Admin View
            if profile.user.is_staff == True:
                return render(request, "pages/home.html")
            # Anonymous View
            if profile.role == 7:
                return render(request, "anonymous.html")
        return render(request, "anonymous.html")
