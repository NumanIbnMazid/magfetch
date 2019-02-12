from django.views.generic import TemplateView
from django.shortcuts import render

class HomeView(TemplateView):
    template_name = 'pages/home.html'

def error_404(request):
    data = {}
    return render(request,'404.html', data)

def error_500(request):
    data = {}
    return render(request,'404.html', data)
