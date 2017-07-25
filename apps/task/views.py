from datetime import datetime
from math import floor

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from apps.task.forms import TaskForm
from apps.task.models import Task

"""
Task views created to manage the task CRUD operation.
"""


class TaskIndexView(LoginRequiredMixin, ListView):
	"""
	View that is used to show all the tasks that exist in the Chronos platform.
	Receives optional parameters to show alert functions:
	@param result (optional) - Shows alert functions accordingly

		Task added - YWRkZWQ=
		Task edited - ZWRpdGVk
		Task deleted - ZGVsZXRlZA==

	TODO: Develop this view
	"""

	template_name = 'task/task_index.html'
	model = Task

	def get_alert_information(self):
		if 'result' in self.kwargs:
			if self.kwargs['result'] == 'YWRkZWQ=':
				return _("A new task was added with success!")
			if self.kwargs['result'] == 'ZWRpdGVk':
				return _("The task information was edited with success!")
			if self.kwargs['result'] == 'ZGVsZXRlZA==':
				return _("The task information was deleted with success!")

	def get_context_data(self, **kwargs):
		context = super(TaskIndexView, self).get_context_data(**kwargs)
		context['page_title'] = _('Task list - CHRONOS')
		context['task_active'] = 'active open'
		context['task_viewall_active'] = 'active'
		context['result'] = self.get_alert_information()

		return context


class TaskDetailView(LoginRequiredMixin, DetailView):
	"""
	View that is used to show the task information that exists in the Chronos platform.
	TODO: Develop this view
	"""

	template_name = "task/task_base.html"
	model = Task

	def get_context_data(self, **kwargs):
		context = super(TaskDetailView, self).get_context_data(**kwargs)
		context['page_title'] = _('Task detail - CHRONOS')
		context['task_active'] = 'active open'
		context['task_viewall_active'] = 'active'
		context['progress'] = self.get_profile_completion()

		return context

	# This function is used to calculate the total percentage of the task's profile completion.
	def get_profile_completion(self):
		task = self.get_object()
		filled_fields = 0
		total_fields = len(task._meta.fields)

		for field in task._meta.fields:
			if getattr(task, field.name):
				filled_fields += 1

		progression = floor((filled_fields / total_fields) * 100)

		return progression


class TaskAddView(LoginRequiredMixin, CreateView):
	"""
	View that is used to add a new task in the Chronos platform.
	TODO: Develop this view
	"""

	model = Task
	form_class = TaskForm
	template_name = 'task/task_form.html'

	def get_context_data(self, **kwargs):
		context = super(TaskAddView, self).get_context_data(**kwargs)
		context['page_title'] = _('Add new task - CHRONOS')
		context['title'] = _('Add a new task')
		context['task_active'] = 'active open'
		context['task_add_active'] = 'active'
		context['task_list'] = self.get_queryset()
		context['is_new_task'] = True
		context['tasks'] = Task.objects.values_list('id', 'name').order_by('name')

		return context

	def form_valid(self, form):
		return super(TaskAddView, self).form_valid(form)

	def get_success_url(self):
		return reverse_lazy('task:index', kwargs={'result': 'YWRkZWQ='})


class TaskEditView(LoginRequiredMixin, UpdateView):
	"""
	View that is used to add a new task in the Chronos platform.
	TODO: Develop this view
	"""

	model = Task
	form_class = TaskForm
	template_name = 'task/task_form.html'

	def get_context_data(self, **kwargs):
		context = super(TaskEditView, self).get_context_data(**kwargs)
		context['page_title'] = _('Edit task - CHRONOS')
		context['title'] = _('Edit task')
		context['task_active'] = 'active open'
		context['task_viewall_active'] = 'active'
		context['is_new_task'] = False

		return context

	def form_valid(self, form):
		form.instance.last_updated = datetime.now()
		return super(TaskEditView, self).form_valid(form)

	def get_success_url(self):
		return reverse_lazy('task:index', kwargs={'result': 'ZWRpdGVk'})


class TaskDeleteView(LoginRequiredMixin, DeleteView):
	model = Task
	template_name = 'task/task_delete_modal.html'

	def dispatch(self, *args, **kwargs):

		id = self.get_object().id

		response = super(TaskDeleteView, self).dispatch(*args, **kwargs)
		if self.request.is_ajax():
			response_data = {"result": "ok", "id": id}
			return JsonResponse(response_data)
		else:
			# POST request (not ajax) will do a redirect to success_url
			return response

	def get_success_url(self):
		return reverse_lazy('task:index', kwargs={'result': 'ZGVsZXRlZA=='})
