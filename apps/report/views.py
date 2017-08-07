import time
import os

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib.colors import grey, white, black

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.utils.translation import ugettext_lazy as _
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.db.models import Q

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

    def report_entryreportpdf(self, report_type):

        # standard distance for report
        margin = 1.5

        # Create the PDF object
        timestamp = int(time.time())
        filename = report_type + str(timestamp)
        pdf_report = SimpleDocTemplate('reports/{0}.pdf'.format(filename), author="Chronos Platform",
                                       rightMargin=margin*cm, leftMargin=margin*cm, topMargin=margin*cm,
                                       bottomMargin=margin*cm, pagesize=landscape(A4))
        request = self.request

        qdict = {'starttime': 'starttime__gte',
                 'endtime': 'endtime__lte',
                 'task': 'task',
                 'user': 'user',
                 'client': 'client',
                 'project': 'project',
                 }

        q_objs = [Q(**{qdict[k]: request.POST.get(k)}) for k in qdict.keys() if request.POST.get(k, None)]

        # Fetch all entries
        entries = Entry.objects.select_related().filter(*q_objs)

        # Generate the table
        table_data = [['Description', 'Start time', 'End time', 'Duration (min.)', 'Comments', 'Project', 'Client',
                       'User']]

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

        table = Table(table_data)
        table.setStyle(TableStyle(
            [
                ('BACKGROUND', (0, 0), (7, 0), grey),
                ('TEXTCOLOR', (0, 0), (7, 0), white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('INNERGRID', (0, 0), (-1, -1), 0.25, black),
                ('BOX', (0, 0), (-1, -1), 0.25, black),
            ]
        ))
        styles = getSampleStyleSheet()

        elements = []

        elements.append(Paragraph(_('Chronos entries report'), styles['Heading1']))
        elements.append(Spacer(36, 20))
        elements.append(Paragraph(_('Report created using Chronos platform'), styles['Heading2']))
        elements.append(Paragraph(_('Generated on %s') % time.ctime(time.time()), styles['Normal']))
        elements.append(Spacer(36, 20))
        elements.append(table)

        # Build the report
        pdf_report.build(elements)

        fs = FileSystemStorage("reports")

        with fs.open("{0}.pdf".format(filename)) as pdf_report:
            Report.objects.create(
                name="{0}.pdf".format(filename),
                type=report_type,
                file=pdf_report,
                filetype='pdf',
                user=self.request.user
            )

        os.remove("reports/{0}.pdf".format(filename))
        data = {
            'result': 'report_generated',
        }
        return JsonResponse(data)

    def switch(self, report_type):

        method_name = 'report_' + str(report_type)

        def default(x, y):
            return "no report defined"

        # Get the method from 'self'. Default to a lambda.
        method = getattr(self, method_name, default)

        # Call the method as we return it
        return method(report_type)

    def post(self, request, *args, **kwargs):

        report_type = request.POST.get('report_type')
        return self.switch(report_type)


class DownloadReportView (LoginRequiredMixin, TemplateView):

    def post(self, request, *args, **kwargs):

        report = Report.objects.get(pk=self.request.POST.get('pk'))

        fs = FileSystemStorage('/')
        with fs.open(report.file.url) as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="{0}"'.format(report.name)
            return response
