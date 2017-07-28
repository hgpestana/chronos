from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView
from django.db.models import Count

from apps.entry.models import Entry
from apps.client.models import Client
from apps.project.models import Project
from apps.task.models import Task

"""
Main views for the Chronos platform
"""


class CoreIndexView(LoginRequiredMixin, TemplateView):
	"""
	View that is used to show the Chronos dashboard
	TODO: Develop this view
	"""
	template_name = 'core/dashboard.html'

	def get_context_data(self, **kwargs):
		context = super(CoreIndexView, self).get_context_data(**kwargs)
		context['page_title'] = _('Dashboard - CHRONOS')
		context['dashboard'] = 'active'
		context['totals'] = self.get_totals_user()
		return context

	def get_totals_user(self):

		totals = {}

		try:
			totals['user_entries'] = Entry.objects.filter(user=self.request.user).count()
		except Entry.DoesNotExist:
			totals['user_entries'] = 0

		try:
			totals['user_clients'] = Entry.objects.filter(user=self.request.user).filter(client__isnull=False).values(
				'client').distinct().count()
		except Entry.DoesNotExist:
			totals['user_clients'] = 0

		try:
			totals['user_projects'] = Entry.objects.filter(user=self.request.user).filter(project__isnull=False).values(
				'project').distinct().count()
		except Entry.DoesNotExist:
			totals['user_projects'] = 0

		try:
			totals['user_tasks'] = Entry.objects.filter(user=self.request.user).filter(task__isnull=False).values(
				'task').distinct().count()
		except Entry.DoesNotExist:
			totals['user_tasks'] = 0

		totals['entries'] = Entry.objects.all().count()
		totals['clients'] = Client.objects.all().count()
		totals['projects'] = Project.objects.all().count()
		totals['tasks'] = Task.objects.all().count()

		try:
			totals['user_entries_percent'] = (totals['user_entries'] / totals['entries']) * 100
		except ZeroDivisionError:
			totals['user_entries_percent'] = 0

		try:
			totals['user_clients_percent'] = (totals['user_clients'] / totals['clients']) * 100
		except ZeroDivisionError:
			totals['user_clients_percent'] = 0

		try:
			totals['user_projects_percent'] = (totals['user_projects'] / totals['projects']) * 100
		except ZeroDivisionError:
			totals['user_projects_percent'] = 0

		try:
			totals['user_tasks_percent'] = (totals['user_tasks'] / totals['tasks']) * 100
		except ZeroDivisionError:
			totals['user_tasks_percent'] = 0

		totals['user_per_client_entries'] = Entry.objects.all().filter(user=self.request.user).filter(
			client__isnull=False).values('client__name').annotate(Count('client', distinct=True))

		totals['user_per_task_entries'] = Entry.objects.all().filter(user=self.request.user).filter(
			task__isnull=False).values('task__name').annotate(Count('task', distinct=True))

		totals['user_per_project_entries'] = Entry.objects.all().filter(user=self.request.user).filter(
			project__isnull=False).values('project__name').annotate(Count('project', distinct=True))

		return totals




def error404(request):
	return render(request, 'errors/404.html')


def error500(request):
	return render(request, 'errors/500.html')
