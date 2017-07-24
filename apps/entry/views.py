from django.utils.translation import ugettext_lazy as _
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.urls import reverse_lazy

from math import floor
from datetime import datetime

from apps.entry.models import Entry
from apps.entry.forms import EntryForm

"""
Entry views created to manage the entry CRUD operation.
"""


class EntryIndexView(LoginRequiredMixin, ListView):
    """
    View that is used to show all the entries that exist in the Chronos platform.
    Receives optional parameters to show alert functions:
    @param result (optional) - Shows alert functions accordingly

        Entry added - YWRkZWQ=
        Entry edited - ZWRpdGVk
        Entry deleted - ZGVsZXRlZA==

    TODO: Develop this view
    """
    template_name = 'entry/entry_index.html'
    model = Entry

    def get_alert_information(self):
        if 'result' in self.kwargs:
            if self.kwargs['result'] == 'YWRkZWQ=':
                return _("A new entry was added with success!")
            if self.kwargs['result'] == 'ZWRpdGVk':
                return _("The entry information was edited with success!")
            if self.kwargs['result'] == 'ZGVsZXRlZA==':
                return _("The entry information was deleted with success!")

    def get_context_data(self, **kwargs):
        context = super(EntryIndexView, self).get_context_data(**kwargs)
        context['page_title'] = _('Entry list - CHRONOS')
        context['entry_active'] = 'active open'
        context['entry_viewall_active'] = 'active'
        context['result'] = self.get_alert_information()

        return context


class EntryDetailView(LoginRequiredMixin, DetailView):
    """
    View that is used to show the entry information that exists in the Chronos platform.
    TODO: Develop this view
    """
    template_name = "entry/entry_base.html"
    model = Entry

    def get_context_data(self, **kwargs):
        context = super(EntryDetailView, self).get_context_data(**kwargs)
        context['page_title'] = _('Entry detail - CHRONOS')
        context['entry_active'] = 'active open'
        context['entry_viewall_active'] = 'active'
        context['progress'] = self.get_profile_completion()

        return context

    # This function is used to calculate the total percentage of the entry's profile completion.
    def get_profile_completion(self):
        entry = self.get_object()
        filled_fields = 0
        total_fields = len(entry._meta.fields)

        for field in entry._meta.fields:
            if getattr(entry, field.name):
                    filled_fields += 1

        progression = floor((filled_fields / total_fields) * 100)

        return progression


class EntryAddView(LoginRequiredMixin, CreateView):
    """
    View that is used to add a new entry in the Chronos platform.
    TODO: Develop this view
    """
    model = Entry
    form_class = EntryForm
    template_name = 'entry/entry_form.html'

    def get_context_data(self, **kwargs):
        context = super(EntryAddView, self).get_context_data(**kwargs)
        context['page_title'] = _('Add new entry - CHRONOS')
        context['title'] = _('Add a new entry')
        context['entry_active'] = 'active open'
        context['entry_add_active'] = 'active'
        context['is_new_entry'] = True

        return context

    def form_valid(self, form):
        #form.instance.duration = (form.instance.endtime - form.instance.starttime)/60000
        #form.save()
        return super(EntryAddView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('entry:index', kwargs={'result': 'YWRkZWQ='})


class EntryEditView(LoginRequiredMixin, UpdateView):
    """
    View that is used to add a new entry in the Chronos platform.
    TODO: Develop this view
    """
    model = Entry
    form_class = EntryForm
    template_name = 'entry/entry_form.html'

    def get_context_data(self, **kwargs):
        context = super(EntryEditView, self).get_context_data(**kwargs)
        context['page_title'] = _('Edit entry - CHRONOS')
        context['title'] = _('Edit entry')
        context['entry_active'] = 'active open'
        context['entry_viewall_active'] = 'active'
        context['is_new_entry'] = False

        return context

    def form_valid(self, form):
        form.instance.last_updated = datetime.now()
        return super(EntryEditView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('entry:index', kwargs={'result': 'ZWRpdGVk'})


class EntryDeleteView(LoginRequiredMixin, DeleteView):

    model = Entry
    template_name = 'entry/entry_delete_modal.html'

    def dispatch(self, *args, **kwargs):

        id = self.get_object().id

        response = super(EntryDeleteView, self).dispatch(*args, **kwargs)
        if self.request.is_ajax():
            response_data = {"result": "ok", "id": id}
            return JsonResponse(response_data)
        else:
            # POST request (not ajax) will do a redirect to success_url
            return response

    def get_success_url(self):
        return reverse_lazy('entry:index', kwargs={'result': 'ZGVsZXRlZA=='})