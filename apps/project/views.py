from datetime import datetime
from math import floor

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from apps.project.forms import ProjectForm
from apps.project.models import Project

"""
Project views created to manage the project CRUD operation.
"""


class ProjectIndexView(LoginRequiredMixin, ListView):
	"""
	View that is used to show all the projects that exist in the Chronos platform.
	Receives optional parameters to show alert functions:
	@param result (optional) - Shows alert functions accordingly

		Project added - YWRkZWQ=
		Project edited - ZWRpdGVk
		Project deleted - ZGVsZXRlZA==

	TODO: Develop this view
	"""

	template_name = 'project/project_index.html'
	model = Project

	def get_alert_information(self):
		if 'result' in self.kwargs:
			if self.kwargs['result'] == 'YWRkZWQ=':
				return _("A new project was added with success!")
			if self.kwargs['result'] == 'ZWRpdGVk':
				return _("The project information was edited with success!")
			if self.kwargs['result'] == 'ZGVsZXRlZA==':
				return _("The project information was deleted with success!")

	def get_context_data(self, **kwargs):
		context = super(ProjectIndexView, self).get_context_data(**kwargs)
		context['page_title'] = _('Project list - CHRONOS')
		context['project_active'] = 'active open'
		context['project_viewall_active'] = 'active'
		context['result'] = self.get_alert_information()

		return context


class ProjectDetailView(LoginRequiredMixin, DetailView):
	"""
	View that is used to show the project information that exists in the Chronos platform.
	TODO: Develop this view
	"""

	template_name = "project/project_base.html"
	model = Project

	def get_context_data(self, **kwargs):
		context = super(ProjectDetailView, self).get_context_data(**kwargs)
		context['page_title'] = _('Project detail - CHRONOS')
		context['project_active'] = 'active open'
		context['project_viewall_active'] = 'active'
		context['progress'] = self.get_profile_completion()

		return context

	# This function is used to calculate the total percentage of the project's profile completion.
	def get_profile_completion(self):
		project = self.get_object()
		filled_fields = 0
		total_fields = len(project._meta.fields)

		for field in project._meta.fields:
			if getattr(project, field.name):
				filled_fields += 1

		progression = floor((filled_fields / total_fields) * 100)

		return progression


class ProjectAddView(LoginRequiredMixin, CreateView):
	"""
	View that is used to add a new project in the Chronos platform.
	TODO: Develop this view
	"""

	model = Project
	form_class = ProjectForm
	template_name = 'project/project_form.html'

	def get_context_data(self, **kwargs):
		context = super(ProjectAddView, self).get_context_data(**kwargs)
		context['page_title'] = _('Add new project - CHRONOS')
		context['title'] = _('Add a new project')
		context['project_active'] = 'active open'
		context['project_add_active'] = 'active'
		context['project_list'] = self.get_queryset()
		context['is_new_project'] = True

		return context

	def form_valid(self, form):
		return super(ProjectAddView, self).form_valid(form)

	def get_success_url(self):
		return reverse_lazy('project:index', kwargs={'result': 'YWRkZWQ='})


class ProjectEditView(LoginRequiredMixin, UpdateView):
	"""
	View that is used to add a new project in the Chronos platform.
	TODO: Develop this view
	"""

	model = Project
	form_class = ProjectForm
	template_name = 'project/project_form.html'

	def get_context_data(self, **kwargs):
		context = super(ProjectEditView, self).get_context_data(**kwargs)
		context['page_title'] = _('Edit project - CHRONOS')
		context['title'] = _('Edit project')
		context['project_active'] = 'active open'
		context['project_viewall_active'] = 'active'
		context['is_new_project'] = False

		return context

	def form_valid(self, form):
		form.instance.last_updated = datetime.now()
		return super(ProjectEditView, self).form_valid(form)

	def get_success_url(self):
		return reverse_lazy('project:index', kwargs={'result': 'ZWRpdGVk'})


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
	model = Project
	template_name = 'project/project_delete_modal.html'

	def dispatch(self, *args, **kwargs):

		id = self.get_object().id

		response = super(ProjectDeleteView, self).dispatch(*args, **kwargs)
		if self.request.is_ajax():
			response_data = {"result": "ok", "id": id}
			return JsonResponse(response_data)
		else:
			# POST request (not ajax) will do a redirect to success_url
			return response

	def get_success_url(self):
		return reverse_lazy('project:index', kwargs={'result': 'ZGVsZXRlZA=='})
