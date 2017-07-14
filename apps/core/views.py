from django.http import HttpResponse
from django.template import loader

# Create your views here.

def index(request):
    template = loader.get_template('core/dashboard.html')
    context = {
        'page_title': 'Dashboard - CHRONOS',
        'dashboard_active': 'active',
    }
    return HttpResponse(template.render(context, request))

def error404(request):
    return render(request, 'errors/404.html')

def error500(request):
    return render(request, 'errors/500.html')