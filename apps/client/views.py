from django.utils.translation import ugettext_lazy as _
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.urls import reverse_lazy
from math import floor

from datetime import datetime

from apps.client.models import TClient
from apps.client.forms import ClientForm

class ClientIndexView(ListView):
    """
    View that is used to show all the clients that exist in the Chronos platform.
    TODO: Develop this view
    """
    template_name = 'client/client_index.html'
    model = TClient

    def get_context_data(self, **kwargs):
        context = super(ClientIndexView, self).get_context_data(**kwargs)
        context['page_title'] = _('Client list - CHRONOS')
        context['client_active'] = 'active open'
        context['client_viewall_active'] = 'active'

        return context


class ClientDetailView(DetailView):
    """
    View that is used to show the client information that exists in the Chronos platform.
    TODO: Develop this view
    """
    template_name = "client/client_base.html"
    model = TClient

    def get_context_data(self, **kwargs):
        context = super(ClientDetailView, self).get_context_data(**kwargs)
        context['page_title'] = _('Client detail - CHRONOS')
        context['client_active'] = 'active open'
        context['client_viewall_active'] = 'active'
        context['progress'] = self.get_profile_completion()

        return context

    # This function is used to calculate the total percentage of the client's profile completion.
    def get_profile_completion(self):
        client = self.get_object()
        filled_fields = 0
        total_fields = len(client._meta.fields)

        for field in client._meta.fields:
            if getattr(client, field.name):
                    filled_fields += 1

        progression = floor((filled_fields / total_fields) * 100)

        return progression


class ClientAddView(CreateView):
    """
    View that is used to add a new client in the Chronos platform.
    TODO: Develop this view
    """
    model = TClient
    form_class = ClientForm
    template_name = 'client/client_form.html'

    def get_context_data(self, **kwargs):
        context = super(ClientAddView, self).get_context_data(**kwargs)
        context['page_title'] = _('Add new client - CHRONOS')
        context['title'] = _('Add a new client')
        context['client_active'] = 'active open'
        context['client_add_active'] = 'active'
        context['client_list'] = self.get_queryset()
        context['is_new_client'] = True

        return context

    def form_valid(self, form):
        form.instance.last_updated = datetime.now()
        return super(ClientAddView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('client:index')


class ClientEditView(UpdateView):
    """
    View that is used to add a new client in the Chronos platform.
    TODO: Develop this view
    """
    model = TClient
    form_class = ClientForm
    template_name = 'client/client_form.html'

    def get_context_data(self, **kwargs):
        context = super(ClientEditView, self).get_context_data(**kwargs)
        context['page_title'] = _('Edit client - CHRONOS')
        context['title'] = _('Edit client')
        context['client_active'] = 'active open'
        context['client_viewall_active'] = 'active'
        context['is_new_client'] = False

        return context

    def form_valid(self, form):
        form.instance.last_updated = datetime.now()
        return super(ClientEditView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('client:index')


class ClientDeleteView(DeleteView):

    model = TClient
    template_name = 'client/client_delete_modal.html'

    def dispatch(self, *args, **kwargs):

        id = self.get_object().id

        response = super(ClientDeleteView, self).dispatch(*args, **kwargs)
        if self.request.is_ajax():
            response_data = {"result": "ok", "id": id}
            return JsonResponse(response_data)
        else:
            # POST request (not ajax) will do a redirect to success_url
            return response

    def get_success_url(self):
        return reverse_lazy('client:index')