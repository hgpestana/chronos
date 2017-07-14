from django.shortcuts import get_object_or_404, render
from django.utils.translation import ugettext_lazy as _
from django.views.generic.list import ListView
from django.http import HttpResponseRedirect
from django.urls import reverse

from apps.project.models import TProject

class IndexView(ListView):
    template_name = 'project/project.html'
    model = TProject

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['page_title'] = _('Project list - CHRONOS')
        context['project_active'] = 'active open'
        context['project_viewall_active'] = 'active'
        context['project_list'] = self.get_queryset()

        return context