from django.views.generic import TemplateView
from django.shortcuts import render

class HomeView(TemplateView):
    template_name = 'pages/home.html'

def handler404(request):
    return render(request, '404.html', status=404)