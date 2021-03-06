from datetime import datetime
from math import floor

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import password_validators_help_texts
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from apps.account.forms import UserForm, AccountForm

"""
Account views created to manage the account CRUD operation.
"""


class AccountIndexView(LoginRequiredMixin, ListView):
	"""
	View that is used to show all the accounts that exist in the Chronos platform.
	Receives optional parameters to show alert functions:
	@param result (optional) - Shows alert functions accordingly

		Account added - YWRkZWQ=
		Account edited - ZWRpdGVk
		Account deleted - ZGVsZXRlZA==

	TODO: Develop this view
	"""

	template_name = 'account/account_index.html'
	model = User

	def get_alert_information(self):
		"""
		Function used to generate the alert string based on the return result by URL
		:return: String containing the result message
		"""
		if 'result' in self.kwargs:
			if self.kwargs['result'] == 'YWRkZWQ=':
				return _("A new user was added with success!")
			if self.kwargs['result'] == 'ZWRpdGVk':
				return _("The user information was edited with success!")
			if self.kwargs['result'] == 'ZGVsZXRlZA==':
				return _("The user information was deleted with success!")

	def get_context_data(self, **kwargs):
		context = super(AccountIndexView, self).get_context_data(**kwargs)
		context['page_title'] = _('User list - CHRONOS')
		context['account_active'] = 'active open'
		context['account_viewall_active'] = 'active'
		context['result'] = self.get_alert_information()

		return context


class AccountDetailView(LoginRequiredMixin, DetailView):
	"""
	View that is used to show the account information that exists in the Chronos platform.
	TODO: Develop this view
	"""

	template_name = "account/account_base.html"
	model = User

	def get_context_data(self, **kwargs):
		context = super(AccountDetailView, self).get_context_data(**kwargs)
		context['page_title'] = _('User detail - CHRONOS')
		context['account_active'] = 'active open'
		context['account_viewall_active'] = 'active'
		context['progress'] = self.get_profile_completion()

		return context

	def get_profile_completion(self):
		"""
		This function is used to calculate the total percentage of the account's profile completion.
		:return: the calculated percentage
		"""
		account = self.get_object()
		filled_fields = 0
		total_fields = len(account._meta.fields)

		for field in account._meta.fields:
			if getattr(account, field.name):
				filled_fields += 1

		progression = floor((filled_fields / total_fields) * 100)

		return progression


class AccountAddView(LoginRequiredMixin, CreateView):
	"""
	View that is used to add a new account in the Chronos platform.
	TODO: Develop this view
	"""

	model = User
	form_class = UserForm
	template_name = 'account/account_form.html'

	def get_context_data(self, **kwargs):
		context = super(AccountAddView, self).get_context_data(**kwargs)
		context['page_title'] = _('Add new user - CHRONOS')
		context['title'] = _('Add a new user')
		context['account_active'] = 'active open'
		context['account_add_active'] = 'active'
		context['account_list'] = self.get_queryset()
		context['is_new_account'] = True
		context['help_text'] = password_validators_help_texts()

		if self.request.POST:
			context['accountform'] = AccountForm(self.request.POST)
		else:
			context['accountform'] = AccountForm()

		return context

	def form_valid(self, form):
		context = self.get_context_data()
		accountform = context['accountform']

		if accountform.is_valid() and form.is_valid():
			accountform.instance.user = form.save()
			accountform.save()

		return super(AccountAddView, self).form_valid(form)

	def get_success_url(self):
		return reverse_lazy('account:index', kwargs={'result': 'YWRkZWQ='})


class AccountEditView(LoginRequiredMixin, UpdateView):
	"""
	View that is used to edit an account in the Chronos platform.
	TODO: Develop this view
	"""

	model = User
	form_class = UserForm
	template_name = 'account/account_form.html'

	def get_context_data(self, **kwargs):
		context = super(AccountEditView, self).get_context_data(**kwargs)
		context['page_title'] = _('Edit user - CHRONOS')
		context['title'] = _('Edit user')
		context['account_active'] = 'active open'
		context['account_viewall_active'] = 'active'
		context['is_new_account'] = False
		context['help_text'] = password_validators_help_texts()

		if self.request.POST:
			context['accountform'] = AccountForm(self.request.POST, instance=self.get_object().account)
		else:
			context['accountform'] = AccountForm(instance=self.get_object().account)

		return context

	def form_valid(self, form):
		context = self.get_context_data()
		accountform = context['accountform']

		if accountform.is_valid() and form.is_valid():
			accountform.instance.last_updated = datetime.now()
			accountform.save()

		return super(AccountEditView, self).form_valid(form)

	def get_success_url(self):
		return reverse_lazy('account:index', kwargs={'result': 'ZWRpdGVk'})


class AccountDeleteView(LoginRequiredMixin, DeleteView):
	"""
	View that is used to delete an account in the Chronos platform. Accessed via AJAX call
	TODO: Develop this view
	"""
	model = User
	template_name = 'account/account_delete_modal.html'

	def dispatch(self, *args, **kwargs):

		response = super(AccountDeleteView, self).dispatch(*args, **kwargs)
		if self.request.is_ajax():
			response_data = {"result": "ok"}
			return JsonResponse(response_data)
		else:
			# POST request (not ajax) will do a redirect to success_url
			return response

	def get_success_url(self):
		return reverse_lazy('account:index', kwargs={'result': 'ZGVsZXRlZA=='})
