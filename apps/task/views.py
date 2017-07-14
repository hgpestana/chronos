from django.shortcuts import get_object_or_404, render
from django.utils.translation import ugettext_lazy as _
from django.views.generic.list import ListView
from django.http import HttpResponseRedirect
from django.urls import reverse

from apps.task.models import TTask

class IndexView(ListView):
    template_name = 'task/task.html'
    model = TTask

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['page_title'] = _('Task list - CHRONOS')
        context['task_active'] = 'active open'
        context['task_viewall_active'] = 'active'
        context['task_list'] = self.get_queryset()

        return context