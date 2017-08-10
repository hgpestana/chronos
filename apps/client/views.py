from datetime import datetime
from math import floor

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from apps.client.forms import ClientForm
from apps.client.models import Client

"""
Client views created to manage the client CRUD operation.
"""


class ClientIndexView(LoginRequiredMixin, ListView):
	"""
	View that is used to show all the clients that exist in the Chronos platform.
	Receives optional parameters to show alert functions:
	@param result (optional) - Shows alert functions accordingly

		Client added - YWRkZWQ=
		Client edited - ZWRpdGVk
		Client deleted - ZGVsZXRlZA==

	TODO: Develop this view
	"""

	template_name = 'client/client_index.html'
	model = Client

	def get_alert_information(self):
		"""
		Function used to generate the alert string based on the return result by URL
		:return: String containing the result message
		"""
		if 'result' in self.kwargs:
			if self.kwargs['result'] == 'YWRkZWQ=':
				return _("A new client was added with success!")
			if self.kwargs['result'] == 'ZWRpdGVk':
				return _("The client information was edited with success!")
			if self.kwargs['result'] == 'ZGVsZXRlZA==':
				return _("The client information was deleted with success!")

	def get_context_data(self, **kwargs):
		context = super(ClientIndexView, self).get_context_data(**kwargs)
		context['page_title'] = _('Client list - CHRONOS')
		context['client_active'] = 'active open'
		context['client_viewall_active'] = 'active'
		context['result'] = self.get_alert_information()

		return context


class ClientDetailView(LoginRequiredMixin, DetailView):
	"""
	View that is used to show the client information that exists in the Chronos platform.
	TODO: Develop this view
	"""

	template_name = "client/client_base.html"
	model = Client

	def get_context_data(self, **kwargs):
		context = super(ClientDetailView, self).get_context_data(**kwargs)
		context['page_title'] = _('Client detail - CHRONOS')
		context['client_active'] = 'active open'
		context['client_viewall_active'] = 'active'
		context['progress'] = self.get_profile_completion()

		return context

	def get_profile_completion(self):
		"""
		This function is used to calculate the total percentage of the client's profile completion.
		:return: the calculated percentage
		"""
		client = self.get_object()
		filled_fields = 0
		total_fields = len(client._meta.fields)

		for field in client._meta.fields:
			if getattr(client, field.name):
				filled_fields += 1

		progression = floor((filled_fields / total_fields) * 100)

		return progression


class ClientAddView(LoginRequiredMixin, CreateView):
	"""
	View that is used to add a new client in the Chronos platform.
	TODO: Develop this view
	"""

	model = Client
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
		return super(ClientAddView, self).form_valid(form)

	def get_success_url(self):
		return reverse_lazy('client:index', kwargs={'result': 'YWRkZWQ='})


class ClientEditView(LoginRequiredMixin, UpdateView):
	"""
	View that is used to edit a client in the Chronos platform.
	TODO: Develop this view
	"""

	model = Client
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
		return reverse_lazy('client:index', kwargs={'result': 'ZWRpdGVk'})


class ClientDeleteView(LoginRequiredMixin, DeleteView):
	"""
	View that is used to delete a client in the Chronos platform. Accessed via AJAX call
	TODO: Develop this view
	"""
	model = Client
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
		return reverse_lazy('client:index', kwargs={'result': 'ZGVsZXRlZA=='})
