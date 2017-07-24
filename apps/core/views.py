from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

"""
Main views for the Chronos platform
"""


class CoreIndexView(LoginRequiredMixin, TemplateView):
    """
    View that is used to show the Chronos dashboard
    TODO: Develop this view
    """
    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(CoreIndexView, self).get_context_data(**kwargs)
        context['page_title'] = _('Dashboard - CHRONOS')
        context['dashboard'] = 'active'

        return context


def error404(request):
    return render(request, 'errors/404.html')


def error500(request):
    return render(request, 'errors/500.html')