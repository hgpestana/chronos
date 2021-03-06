from datetime import datetime
from math import floor
from decimal import Decimal

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib.auth.models import User
from django.db.models import Q

from apps.entry.forms import EntryForm
from apps.entry.models import Entry

from apps.client.models import Client
from apps.project.models import Project
from apps.task.models import Task

"""
Entry views created to manage the entry CRUD operation.
"""


class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """

    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'result': 'Data saved with success!',
            }
            return JsonResponse(data)
        else:
            return response


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

    def get_queryset(self):
        return Entry.objects.filter(
            Q(task__is_visible=True) | Q(task__isnull=True),
            Q(project__is_visible=True) | Q(project__isnull=True),
            Q(client__is_visible=True) | Q(client__isnull=True)
        )

    def get_alert_information(self):
        """
        Function used to generate the alert string based on the return result by URL
        :return: String containing the result message
        """
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
        context['users'] = User.objects.all()
        context['clients'] = Client.objects.all()
        context['tasks'] = Task.objects.all()
        context['projects'] = Project.objects.all()

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

    def get_profile_completion(self):
        """
        This function is used to calculate the total percentage of the entry's profile completion.
        :return: the calculated percentage
        """
        entry = self.get_object()
        filled_fields = 0
        total_fields = len(entry._meta.fields)

        for field in entry._meta.fields:
            if getattr(entry, field.name):
                filled_fields += 1

        progression = floor((filled_fields / total_fields) * 100)

        return progression


class EntryAddView(LoginRequiredMixin, AjaxableResponseMixin,  CreateView):
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
        end_time = form.instance.endtime
        start_time = form.instance.starttime

        if end_time > start_time:
            form.instance.duration = (end_time - start_time).seconds / 60
        else:
            form.instance.duration = 0

        form.instance.user = self.request.user

        if form.instance.task:
            if form.instance.duration > 0:
                task_price_min = form.instance.task.price / 60
                form.instance.cost = Decimal.from_float(form.instance.duration) * task_price_min
            else:
                form.instance.cost = 0
        else:
            form.instance.cost = 0

        return super(EntryAddView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('entry:index', kwargs={'result': 'YWRkZWQ='})


class EntryEditView(LoginRequiredMixin, UpdateView):
    """
    View that is used to edit an entry in the Chronos platform.
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
        end_time = form.instance.endtime
        start_time = form.instance.starttime

        if end_time > start_time:
            form.instance.duration = (end_time - start_time).seconds / 60
        else:
            form.instance.duration = 0

        form.instance.last_updated = datetime.now()

        if form.instance.task:
            if form.instance.duration > 0:
                task_price_min = form.instance.task.price / 60
                form.instance.cost = Decimal.from_float(form.instance.duration) * task_price_min
            else:
                form.instance.cost = 0
        else:
            form.instance.cost = 0

        return super(EntryEditView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('entry:index', kwargs={'result': 'ZWRpdGVk'})


class EntryDeleteView(LoginRequiredMixin, DeleteView):
    """
    View that is used to delete an entry in the Chronos platform. Accessed via AJAX call
    TODO: Develop this view
    """
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
