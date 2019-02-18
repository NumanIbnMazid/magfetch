from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from accounts.models import UserProfile

# @method_decorator(login_required, name='dispatch')
# class HomeView(TemplateView):
#     template_name = 'pages/home.html'


@method_decorator(login_required, name='dispatch')
class HomeView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        user_profile_filter = UserProfile.objects.filter(user=user)
        if user_profile_filter.exists():
            profile = user_profile_filter.first()
            if profile.role == 4:
                return render(request, "landing/pages/home.html")
            if profile.role == 0 or profile.role == 1 or profile.role == 2 or profile.role == 3:
                return render(request, "pages/home.html")
            if profile.user.is_staff == True:
                return render(request, "pages/home.html")
            if profile.role == 7:
                return render(request, "anonymous.html")
        return render(request, "anonymous.html")
