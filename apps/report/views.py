import time

from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus.tables import Table
from reportlab.lib.pagesizes import A4

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage

from apps.report.models import Report
from apps.report.models import ReportType

from apps.client.models import Client
from apps.project.models import Project
from apps.task.models import Task
from apps.entry.models import Entry

"""
Report views created to manage the entry CRUD operation.
"""


class ReportIndexView(LoginRequiredMixin, ListView):
    """
    View that is used to view and request reports to the Chronos platform.
    TODO: Develop this view
    """

    template_name = 'report/report_index.html'
    model = Report

    def get_context_data(self, **kwargs):
        context = super(ReportIndexView, self).get_context_data(**kwargs)
        context['page_title'] = _('Reports - CHRONOS')
        context['report_active'] = 'active open'
        context['report_viewall_active'] = 'active'
        context['report_types'] = ReportType.objects.all()
        context['users'] = User.objects.all()
        context['clients'] = Client.objects.all()
        context['tasks'] = Task.objects.all()
        context['projects'] = Project.objects.all()

        return context


class GenerateReportView(LoginRequiredMixin, TemplateView):
    """
    View that is used to generate the reports to the Chronos platform.
    TODO: Develop this view
    """
    template_name = 'report/report_index.html'

    def switch(self, report_type):

        method_name = 'report_' + str(report_type)

        def default(x, y):
            return "no report defined"

        # Get the method from 'self'. Default to a lambda.
        method = getattr(self, method_name, default)

        # Call the method as we return it
        return method(report_type)

    def report_entryreportpdf(self, report_type):

        # Get the POST variables
        start_date = self.request.POST.get('start_date')
        end_date = self.request.POST.get('end_date')
        task = self.request.POST.get('task')
        user = self.request.POST.get('user')
        client = self.request.POST.get('client')
        project = self.request.POST.get('project')

        # standard distance for report
        cm = 2.54

        # Create the PDF object
        timestamp = int(time.time())
        filename = report_type + str(timestamp)
        pdf_report = SimpleDocTemplate('reports/{0}.pdf'.format(filename), rightMargin=cm, leftMargin=cm, topMargin=cm, bottomMargin=cm,
                                       pagesize=A4)

        # Fetch all entries
        entries = Entry.objects.select_related()

        # Apply filters to entries
        if start_date:
            entries.filter(starttime__gte=start_date)

        if end_date:
            entries.filter(starttime__lte=end_date)

        if task:
            entries.filter(task=task)

        if user:
            entries.filter(user=user)

        if client:
            entries.filter(client=client)

        if project:
            entries.filter(project=project)

        # Generate the table
        table_data = [['Description', 'Start time', 'End time', 'Duration', 'Comments', 'Project', 'Client', 'User']]

        for entry in entries:

            project_name = client_name = username = ''

            if entry.project:
                project_name = entry.project.name
            if entry.client:
                client_name = entry.client.name
            if entry.user:
                username = entry.user.username

            table_data.append([
                entry.description,
                entry.starttime,
                entry.endtime,
                entry.duration,
                entry.comments,
                project_name,
                client_name,
                username
            ])

        elements = []
        table = Table(table_data)
        elements.append(table)

        # Build the report
        pdf_report.build(elements)

        Report.objects.create(name="{0}.pdf".format(filename), type=report_type, filetype='pdf', user=self.request.user)

        fs = FileSystemStorage("reports")
        with fs.open("{0}.pdf".format(filename)) as pdf_report:
            response = HttpResponse(pdf_report, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="{0}.pdf"'.format(filename)
            return response

    def post(self, request, *args, **kwargs):

        report_type = request.POST.get('report_type')
        return self.switch(report_type)
