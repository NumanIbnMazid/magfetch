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
        
        return render(request, "landing/pages/home.html")
