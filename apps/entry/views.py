from django.http import HttpResponse
from django.template import loader

# Create your views here.

def index(request):
    template = loader.get_template('entry/entry.html')
    context = {
        'page_title': 'Entry list - CHRONOS',
        'entry_active': 'active',
    }
    return HttpResponse(template.render(context, request))