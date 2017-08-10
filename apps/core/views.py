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
        """
        Function used to fill out predefined filter fields for the entries, especially related with
        the objects visibility.
        :param request: the form request (optional) in order to fetch the current user as filter
        :return: a list of Q objects for filter
        """
        q_objs = [
            Q(task__is_visible=True) | Q(task__isnull=True),
            Q(project__is_visible=True) | Q(project__isnull=True),
            Q(client__is_visible=True) | Q(client__isnull=True),
        ]

        if request:
            q_objs.append(Q(user=request.user))

        return q_objs

    def get_latest(self):
        """
        Function that fetches and returns the latest 10 tasks, clients and project objects
        created in the Chronos platform
        :return: a list of Querysets
        """
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
        """
        Function that fetches and returns the latest entry submitted by the current user into the
        Chronos platform
        :return: Queryset object
        """
        try:
            return Entry.objects.filter(*self.entry_filter(self.request)).order_by('-starttime')[0]
        except IndexError:
            return None

    def get_totals_user(self):
        """
        Function that calculates and returns the dashboard's current defined KPI for the Chronos platform
        :return: a list of several KPI / gran totals
        """
        totals = {}

        # calculates the total user entries in the platform. Returns 0 if user has no entries.
        try:
            totals['user_entries'] = Entry.objects.filter(*self.entry_filter(self.request)).count()
        except Entry.DoesNotExist:
            totals['user_entries'] = 0

        # Calculates the total user clients with whom the user has worked with in the platform.
        # Returns 0 if user has no entries.
        try:
            totals['user_clients'] = Entry.objects.filter(*self.entry_filter(self.request)).filter(client__isnull=False)\
                .values('client').distinct().count()
        except Entry.DoesNotExist:
            totals['user_clients'] = 0

        # Calculates the total user projects where the user has worked in the platform.
        # Returns 0 if user has no entries.
        try:
            totals['user_projects'] = Entry.objects.filter(*self.entry_filter(self.request)).filter(project__isnull=False)\
                .values('project').distinct().count()
        except Entry.DoesNotExist:
            totals['user_projects'] = 0

        # Calculates the total user tasks that the user has performed in the platform.
        # Returns 0 if user has no entries.
        try:
            totals['user_tasks'] = Entry.objects.filter(*self.entry_filter(self.request)).filter(task__isnull=False)\
                .values('task').distinct().count()
        except Entry.DoesNotExist:
            totals['user_tasks'] = 0

        # Calculates the total entries, clients, projects and tasks existing in the platform that have
        # their visibility active
        totals['entries'] = Entry.objects.all().filter(*self.entry_filter()).count()
        totals['clients'] = Client.objects.all().filter(is_visible=True).count()
        totals['projects'] = Project.objects.all().filter(is_visible=True).count()
        totals['tasks'] = Task.objects.all().filter(is_visible=True).count()

        # Taking into account the user_entries vs the total entries KPIs, calculates the total percentage
        # Returns 0 if user has no entries.
        try:
            totals['user_entries_percent'] = int(round((totals['user_entries'] / totals['entries']) * 100))
        except ZeroDivisionError:
            totals['user_entries_percent'] = 0

        # Taking into account the user_clients vs the total clients KPIs, calculates the total percentage
        # Returns 0 if user has no entries.
        try:
            totals['user_clients_percent'] = int(round((totals['user_clients'] / totals['clients']) * 100))
        except ZeroDivisionError:
            totals['user_clients_percent'] = 0

        # Taking into account the user_projects vs the total projects KPIs, calculates the total percentage
        # Returns 0 if user has no entries.
        try:
            totals['user_projects_percent'] = int(round((totals['user_projects'] / totals['projects']) * 100))
        except ZeroDivisionError:
            totals['user_projects_percent'] = 0

        # Taking into account the user_tasks vs the total tasks KPIs, calculates the total percentage
        # Returns 0 if user has no entries.
        try:
            totals['user_tasks_percent'] = int(round((totals['user_tasks'] / totals['tasks']) * 100))
        except ZeroDivisionError:
            totals['user_tasks_percent'] = 0

        # Calculates and returns the total amount of user entries per client.
        totals['user_per_client_entries'] = Entry.objects.all().filter(*self.entry_filter(self.request)).filter(
            client__isnull=False).values('client__name').annotate(Count('client'))

        # Calculates and returns the total amount of user entries per task.
        totals['user_per_task_entries'] = Entry.objects.all().filter(*self.entry_filter(self.request)).filter(
            task__isnull=False).values('task__name').annotate(Count('task'))

        # Calculates and returns the total amount of user entries per project.
        totals['user_per_project_entries'] = Entry.objects.all().filter(*self.entry_filter(self.request)).filter(
            project__isnull=False).values('project__name').annotate(Count('project'))

        return totals


def error404(request):
    return render(request, 'errors/404.html')


def error500(request):
    return render(request, 'errors/500.html')
