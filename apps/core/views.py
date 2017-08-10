from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView
from django.db.models import Count, Q

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
        context['last_entry'] = self.get_last_entry()
        context['latest'] = self.get_latest()
        context['clients'] = Client.objects.all().filter(is_visible=True)
        context['tasks'] = Task.objects.all().filter(is_visible=True)
        context['projects'] = Project.objects.all().filter(is_visible=True)

        return context

    @staticmethod
    def entry_filter(request=None):
        q_objs = [
            Q(task__is_visible=True) | Q(task__isnull=True),
            Q(project__is_visible=True) | Q(project__isnull=True),
            Q(client__is_visible=True) | Q(client__isnull=True),
        ]

        if request:
            q_objs.append(Q(user=request.user))

        return q_objs

    def get_latest(self):
        latest = {}

        try:
            latest['tasks'] = Task.objects.order_by('id').filter(is_visible=True)[:10]
        except IndexError:
            latest['tasks'] = None

        try:
            latest['clients'] = Client.objects.order_by('id').filter(is_visible=True)[:10]
        except IndexError:
            latest['clients'] = None

        try:
            latest['projects'] = Project.objects.order_by('id').filter(is_visible=True)[:10]
        except IndexError:
            latest['projects'] = None

        return latest

    def get_last_entry(self):
        try:
            return Entry.objects.filter(*self.entry_filter(self.request)).order_by('-starttime')[0]
        except IndexError:
            return None

    def get_totals_user(self):

        totals = {}

        try:
            totals['user_entries'] = Entry.objects.filter(*self.entry_filter(self.request)).count()
        except Entry.DoesNotExist:
            totals['user_entries'] = 0

        try:
            totals['user_clients'] = Entry.objects.filter(*self.entry_filter(self.request)).filter(client__isnull=False)\
                .values('client').distinct().count()
        except Entry.DoesNotExist:
            totals['user_clients'] = 0

        try:
            totals['user_projects'] = Entry.objects.filter(*self.entry_filter(self.request)).filter(project__isnull=False)\
                .values('project').distinct().count()
        except Entry.DoesNotExist:
            totals['user_projects'] = 0

        try:
            totals['user_tasks'] = Entry.objects.filter(*self.entry_filter(self.request)).filter(task__isnull=False)\
                .values('task').distinct().count()
        except Entry.DoesNotExist:
            totals['user_tasks'] = 0

        totals['entries'] = Entry.objects.all().filter(*self.entry_filter()).count()
        totals['clients'] = Client.objects.all().filter(is_visible=True).count()
        totals['projects'] = Project.objects.all().filter(is_visible=True).count()
        totals['tasks'] = Task.objects.all().filter(is_visible=True).count()

        try:
            totals['user_entries_percent'] = int(round((totals['user_entries'] / totals['entries']) * 100))
        except ZeroDivisionError:
            totals['user_entries_percent'] = 0

        try:
            totals['user_clients_percent'] = int(round((totals['user_clients'] / totals['clients']) * 100))
        except ZeroDivisionError:
            totals['user_clients_percent'] = 0

        try:
            totals['user_projects_percent'] = int(round((totals['user_projects'] / totals['projects']) * 100))
        except ZeroDivisionError:
            totals['user_projects_percent'] = 0

        try:
            totals['user_tasks_percent'] = int(round((totals['user_tasks'] / totals['tasks']) * 100))
        except ZeroDivisionError:
            totals['user_tasks_percent'] = 0

        totals['user_per_client_entries'] = Entry.objects.all().filter(*self.entry_filter(self.request)).filter(
            client__isnull=False).values('client__name').annotate(Count('client'))

        totals['user_per_task_entries'] = Entry.objects.all().filter(*self.entry_filter(self.request)).filter(
            task__isnull=False).values('task__name').annotate(Count('task'))

        totals['user_per_project_entries'] = Entry.objects.all().filter(*self.entry_filter(self.request)).filter(
            project__isnull=False).values('project__name').annotate(Count('project'))

        return totals


def error404(request):
    return render(request, 'errors/404.html')


def error500(request):
    return render(request, 'errors/500.html')
