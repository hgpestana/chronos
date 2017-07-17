from django.shortcuts import get_object_or_404, render
from django.utils.translation import ugettext_lazy as _
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.http import HttpResponseRedirect
from django.urls import reverse

from apps.client.models import TClient
from apps.client.forms import ClientForm


class IndexView(ListView):
    template_name = 'client/client.html'
    model = TClient

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['page_title'] = _('Client list - CHRONOS')
        context['client_active'] = 'active open'
        context['client_viewall_active'] = 'active'
        context['client_list'] = self.get_queryset()

        return context


class AddView(CreateView):
    model = TClient
    form_class = ClientForm
    template_name = 'client/client_form.html'

    def get_context_data(self, **kwargs):
        context = super(AddView, self).get_context_data(**kwargs)
        context['page_title'] = _('Add new client - CHRONOS')
        context['client_active'] = 'active open'
        context['client_add_active'] = 'active'
        context['client_list'] = self.get_queryset()

        return context