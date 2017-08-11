import os
import time

from decimal import Decimal

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from reportlab.lib.colors import grey, white, black
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.platypus.tables import Table, TableStyle

from apps.client.models import Client
from apps.entry.models import Entry
from apps.project.models import Project
from apps.report.models import Report
from apps.report.models import ReportType
from apps.task.models import Task

"""
Report views that are used to view, request, download and generate the reports in Chronos Platform
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
		context['report_types'] = ReportType.objects.all().order_by('name')
		context['users'] = User.objects.all().filter(is_active=True).order_by('username')
		context['clients'] = Client.objects.filter(is_visible=True).all().order_by('name')
		context['tasks'] = Task.objects.all().filter(is_visible=True).order_by('name')
		context['projects'] = Project.objects.all().filter(is_visible=True).order_by('name')

		return context


class GenerateReportView(LoginRequiredMixin, TemplateView):
	"""
	View that is used to generate the reports for the Chronos platform.
	TODO: Develop this view
	"""
	template_name = 'report/report_index.html'

	@staticmethod
	def advanced_filter(request):
		"""
		Auxiliary function for advanced filtering
		:param the form request that will be used to fetch the filters:
		:return: an SQL filter using Q objects
		"""
		# Dictionary with advanced filtering
		qdict = {'starttime': 'starttime__gte',
		         'endtime': 'endtime__lte',
		         'task': 'task',
		         'user': 'user',
		         'client': 'client',
		         'project': 'project',
		         }

		q_objs = [Q(**{qdict[k]: request.POST.get(k)}) for k in qdict.keys() if request.POST.get(k, None)]

		q_objs_visibility = [
			Q(task__is_visible=True) | Q(task__isnull=True),
			Q(project__is_visible=True) | Q(project__isnull=True),
			Q(client__is_visible=True) | Q(client__isnull=True),
		]

		q_objs = q_objs + q_objs_visibility

		return q_objs

	def report_entryreportperprojectpdf(self, report_type):
		"""
		Generates a report that groups entries by project. All entries with no defined project are grouped on the
		same page.
		:param report_type: the requested report type
		:return: JSON with the result
		"""

		# standard distance for report
		margin = 1.5

		# Create the PDF object
		timestamp = int(time.time())
		filename = report_type + str(timestamp)
		pdf_report = SimpleDocTemplate('reports/{0}.pdf'.format(filename), author="Chronos Platform",
		                               rightMargin=margin * cm, leftMargin=margin * cm, topMargin=margin * cm,
		                               bottomMargin=margin * cm, pagesize=landscape(A4))
		# Prepares the filters
		q_objs = self.advanced_filter(self.request)

		# Fetch all filtered entries
		entries = Entry.objects.select_related().filter(*q_objs)
		projects = Entry.objects.all().order_by('project').filter(*q_objs).values_list('project', flat=True).distinct()

		# Style element used by the report
		styles = getSampleStyleSheet()

		# Report elements list
		elements = []

		# Sets the Header
		elements.append(Paragraph(_('Chronos entries per project report'), styles['Heading1']))
		elements.append(Spacer(36, 20))
		elements.append(Paragraph(_('Report created using Chronos platform'), styles['Heading2']))
		elements.append(Paragraph(_('Generated on %s') % time.ctime(time.time()), styles['Normal']))
		elements.append(PageBreak())

		# Iterate the projects in order to group entries per project
		# TODO: Is there an easier way to do this? Or maybe more correct?
		for project in projects:

			# Sets the individual page header
			if project is None:
				elements.append(Paragraph(_('Entries with no project defined'), styles['Heading2']))
			else:
				name = Project.objects.get(id=project).name
				elements.append(Paragraph(_('Entries for project "{0}"').format(name), styles['Heading2']))
			elements.append(Spacer(36, 20))
			table_data = [['Description', 'Start time', 'End time', 'Duration (min.)', 'Cost(EUR)', 'Comments', 'Task',
			               'Project', 'Client', 'User']]

			# Variable used to calculate the total cost for the sheet.
			total_cost = Decimal.from_float(0.00)

			# Iterates per entry in order to find the entry that corresponds to the project. When found, the entry
			# is added to the table
			for entry in entries:

				task_name = project_name = client_name = username = ''

				# Special case for the entries that have no project assigned.
				if not entry.project and project is None:

					if entry.task:
						task_name = entry.task.name
					if entry.client:
						client_name = entry.client.name
					if entry.user:
						username = entry.user.username

					total_cost += entry.cost

					table_data.append([
						entry.description,
						entry.starttime,
						entry.endtime,
						entry.duration,
						entry.cost,
						entry.comments,
						task_name,
						project_name,
						client_name,
						username
					])
				# All other cases with project assigned.
				elif entry.project and entry.project.id == project:

					project_name = entry.project.name

					if entry.task:
						task_name = entry.task.name
					if entry.client:
						client_name = entry.client.name
					if entry.user:
						username = entry.user.username

					total_cost += entry.cost

					table_data.append([
						entry.description,
						entry.starttime,
						entry.endtime,
						entry.duration,
						entry.cost,
						entry.comments,
						task_name,
						project_name,
						client_name,
						username
					])

			# Generates the table with the set data
			table = Table(table_data)
			table.setStyle(TableStyle(
				[
					('BACKGROUND', (0, 0), (9, 0), grey),
					('TEXTCOLOR', (0, 0), (9, 0), white),
					('ALIGN', (0, 0), (-1, -1), 'CENTER'),
					('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
					('INNERGRID', (0, 0), (-1, -1), 0.25, black),
					('BOX', (0, 0), (-1, -1), 0.25, black),
				]
			))

			# Appends the table to the report
			elements.append(table)
			elements.append(Spacer(36, 20))
			elements.append(Paragraph(_('Total cost: %s EUR') % total_cost, styles['Heading2']))
			elements.append(PageBreak())

		# Builds the report
		pdf_report.build(elements)

		# Temporarily stores the report in filesystem in order to assign it to the database
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

		# Returns JSON stating that the report was generated. However, for now, the return string is not used.
		data = {
			'result': 'report_generated',
		}
		return JsonResponse(data)

	def report_entryreportpertaskpdf(self, report_type):
		"""
		Generates a report that groups entries by task. All entries with no defined task are grouped on the
		same page.
		:param report_type: the requested report type
		:return: JSON with the result
		"""

		# standard distance for report
		margin = 1.5

		# Create the PDF object
		timestamp = int(time.time())
		filename = report_type + str(timestamp)
		pdf_report = SimpleDocTemplate('reports/{0}.pdf'.format(filename), author="Chronos Platform",
		                               rightMargin=margin * cm, leftMargin=margin * cm, topMargin=margin * cm,
		                               bottomMargin=margin * cm, pagesize=landscape(A4))
		# Prepares the filters
		q_objs = self.advanced_filter(self.request)

		# Fetch all filtered entries
		entries = Entry.objects.select_related().filter(*q_objs)
		tasks = Entry.objects.all().order_by('task').filter(*q_objs).values_list('task', flat=True).distinct()

		# Style element used by the report
		styles = getSampleStyleSheet()

		# Report elements list
		elements = []

		# Sets the Header
		elements.append(Paragraph(_('Chronos entries per task report'), styles['Heading1']))
		elements.append(Spacer(36, 20))
		elements.append(Paragraph(_('Report created using Chronos platform'), styles['Heading2']))
		elements.append(Paragraph(_('Generated on %s') % time.ctime(time.time()), styles['Normal']))
		elements.append(PageBreak())

		# Iterate the tasks in order to group entries per task
		# TODO: Is there an easier way to do this? Or maybe more correct?
		for task in tasks:

			# Sets the individual page header
			if task is None:
				elements.append(Paragraph(_('Entries with no task defined'), styles['Heading2']))
			else:
				name = Task.objects.get(id=task).name
				elements.append(Paragraph(_('Entries for task "{0}"').format(name), styles['Heading2']))
			elements.append(Spacer(36, 20))
			table_data = [['Description', 'Start time', 'End time', 'Duration (min.)', 'Cost(EUR)', 'Comments', 'Task',
			               'Project', 'Client', 'User']]

			# Variable used to calculate the total cost for the sheet.
			total_cost = Decimal.from_float(0.00)

			# Iterates per entry in order to find the entry that corresponds to the task. When found, the entry
			# is added to the table
			for entry in entries:

				task_name = project_name = client_name = username = ''

				# Special case for the entries that have no task assigned.
				if not entry.task and task is None:

					if entry.project:
						project_name = entry.project.name
					if entry.client:
						client_name = entry.client.name
					if entry.user:
						username = entry.user.username

					total_cost += entry.cost

					table_data.append([
						entry.description,
						entry.starttime,
						entry.endtime,
						entry.duration,
						entry.cost,
						entry.comments,
						task_name,
						project_name,
						client_name,
						username
					])
				# All other cases with task assigned.
				elif entry.task and entry.task.id == task:

					task_name = entry.task.name

					if entry.project:
						project_name = entry.project.name
					if entry.client:
						client_name = entry.client.name
					if entry.user:
						username = entry.user.username

					total_cost += entry.cost

					table_data.append([
						entry.description,
						entry.starttime,
						entry.endtime,
						entry.duration,
						entry.cost,
						entry.comments,
						task_name,
						project_name,
						client_name,
						username
					])

			# Generates the table with the set data
			table = Table(table_data)
			table.setStyle(TableStyle(
				[
					('BACKGROUND', (0, 0), (9, 0), grey),
					('TEXTCOLOR', (0, 0), (9, 0), white),
					('ALIGN', (0, 0), (-1, -1), 'CENTER'),
					('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
					('INNERGRID', (0, 0), (-1, -1), 0.25, black),
					('BOX', (0, 0), (-1, -1), 0.25, black),
				]
			))

			# Appends the table to the report
			elements.append(table)
			elements.append(Spacer(36, 20))
			elements.append(Paragraph(_('Total cost: %s EUR') % total_cost, styles['Heading2']))
			elements.append(PageBreak())

		# Builds the report
		pdf_report.build(elements)

		# Temporarily stores the report in filesystem in order to assign it to the database
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

		# Returns JSON stating that the report was generated. However, for now, the return string is not used.
		data = {
			'result': 'report_generated',
		}
		return JsonResponse(data)

	def report_entryreportperuserpdf(self, report_type):
		"""
		Generates a report that groups entries by user. All entries with no defined user are grouped on the
		same page.
		:param report_type: the requested report type
		:return: JSON with the result
		"""

		# standard distance for report
		margin = 1.5

		# Create the PDF object
		timestamp = int(time.time())
		filename = report_type + str(timestamp)
		pdf_report = SimpleDocTemplate('reports/{0}.pdf'.format(filename), author="Chronos Platform",
		                               rightMargin=margin * cm, leftMargin=margin * cm, topMargin=margin * cm,
		                               bottomMargin=margin * cm, pagesize=landscape(A4))
		# Prepares the filters
		q_objs = self.advanced_filter(self.request)

		# Fetch all filtered entries
		entries = Entry.objects.select_related().filter(*q_objs)
		users = Entry.objects.all().order_by('user').filter(*q_objs).values_list('user', flat=True).distinct()

		# Style element used by the report
		styles = getSampleStyleSheet()

		# Report elements list
		elements = []

		# Sets the Header
		elements.append(Paragraph(_('Chronos entries per user report'), styles['Heading1']))
		elements.append(Spacer(36, 20))
		elements.append(Paragraph(_('Report created using Chronos platform'), styles['Heading2']))
		elements.append(Paragraph(_('Generated on %s') % time.ctime(time.time()), styles['Normal']))
		elements.append(PageBreak())

		# Iterate the users in order to group entries per user
		# TODO: Is there an easier way to do this? Or maybe more correct?
		for user in users:

			# Sets the individual page header
			if user is None:
				elements.append(Paragraph(_('Entries with no user defined'), styles['Heading2']))
			else:
				name = User.objects.get(id=user).username
				elements.append(Paragraph(_('Entries for user "{0}"').format(name), styles['Heading2']))
			elements.append(Spacer(36, 20))
			table_data = [['Description', 'Start time', 'End time', 'Duration (min.)', 'Cost(EUR)', 'Comments', 'Task',
			               'Project', 'Client', 'User']]

			# Variable used to calculate the total cost for the sheet.
			total_cost = Decimal.from_float(0.00)

			# Iterates per entry in order to find the entry that corresponds to the user. When found, the entry
			# is added to the table
			for entry in entries:

				task_name = project_name = client_name = username = ''

				# Special case for the entries that have no user assigned.
				if not entry.user and user is None:

					if entry.task:
						task_name = entry.task.name
					if entry.project:
						project_name = entry.project.name
					if entry.client:
						client_name = entry.client.name

					total_cost += entry.cost

					table_data.append([
						entry.description,
						entry.starttime,
						entry.endtime,
						entry.duration,
						entry.cost,
						entry.comments,
						task_name,
						project_name,
						client_name,
						username
					])
				# All other cases with task assigned.
				elif entry.user and entry.user.id == user:

					username = entry.user.username

					if entry.task:
						task_name = entry.task.name
					if entry.project:
						project_name = entry.project.name
					if entry.client:
						client_name = entry.client.name

					total_cost += entry.cost

					table_data.append([
						entry.description,
						entry.starttime,
						entry.endtime,
						entry.duration,
						entry.cost,
						entry.comments,
						task_name,
						project_name,
						client_name,
						username
					])

			# Generates the table with the set data
			table = Table(table_data)
			table.setStyle(TableStyle(
				[
					('BACKGROUND', (0, 0), (9, 0), grey),
					('TEXTCOLOR', (0, 0), (9, 0), white),
					('ALIGN', (0, 0), (-1, -1), 'CENTER'),
					('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
					('INNERGRID', (0, 0), (-1, -1), 0.25, black),
					('BOX', (0, 0), (-1, -1), 0.25, black),
				]
			))

			# Appends the table to the report
			elements.append(table)
			elements.append(Spacer(36, 20))
			elements.append(Paragraph(_('Total cost: %s EUR') % total_cost, styles['Heading2']))
			elements.append(PageBreak())

		# Builds the report
		pdf_report.build(elements)

		# Temporarily stores the report in filesystem in order to assign it to the database
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

		# Returns JSON stating that the report was generated. However, for now, the return string is not used.
		data = {
			'result': 'report_generated',
		}
		return JsonResponse(data)

	def report_entryreportperclientpdf(self, report_type):
		"""
		Generates a report that groups entries by client. All entries with no defined client are grouped on the
		same page.
		:param report_type: the requested report type
		:return: JSON with the result
		"""

		# standard distance for report
		margin = 1.5

		# Create the PDF object
		timestamp = int(time.time())
		filename = report_type + str(timestamp)
		pdf_report = SimpleDocTemplate('reports/{0}.pdf'.format(filename), author="Chronos Platform",
		                               rightMargin=margin * cm, leftMargin=margin * cm, topMargin=margin * cm,
		                               bottomMargin=margin * cm, pagesize=landscape(A4))
		# Prepares the filters
		q_objs = self.advanced_filter(self.request)

		# Fetch all filtered entries
		entries = Entry.objects.select_related().filter(*q_objs)
		clients = Entry.objects.all().order_by('client').filter(*q_objs).values_list('client', flat=True).distinct()

		# Style element used by the report
		styles = getSampleStyleSheet()

		# Report elements list
		elements = []

		# Sets the Header
		elements.append(Paragraph(_('Chronos entries per client report'), styles['Heading1']))
		elements.append(Spacer(36, 20))
		elements.append(Paragraph(_('Report created using Chronos platform'), styles['Heading2']))
		elements.append(Paragraph(_('Generated on %s') % time.ctime(time.time()), styles['Normal']))
		elements.append(PageBreak())

		# Iterate the clients in order to group entries per client
		# TODO: Is there an easier way to do this? Or maybe more correct?
		for client in clients:

			# Sets the individual page header
			if client is None:
				elements.append(Paragraph(_('Entries with no client defined'), styles['Heading2']))
			else:
				name = Client.objects.get(id=client).name
				elements.append(Paragraph(_('Entries for client "{0}"').format(name), styles['Heading2']))
			elements.append(Spacer(36, 20))
			table_data = [['Description', 'Start time', 'End time', 'Duration (min.)', 'Cost(EUR)', 'Comments', 'Task',
			               'Project', 'Client', 'User']]

			# Variable used to calculate the total cost for the sheet.
			total_cost = Decimal.from_float(0.00)

			# Iterates per entry in order to find the entry that corresponds to the client. When found, the entry
			# is added to the table
			for entry in entries:

				task_name = project_name = client_name = username = ''

				# Special case for the entries that have no client assigned.
				if not entry.client and client is None:

					if entry.task:
						task_name = entry.task.name
					if entry.project:
						project_name = entry.project.name
					if entry.user:
						username = entry.user.username

					total_cost += entry.cost

					table_data.append([
						entry.description,
						entry.starttime,
						entry.endtime,
						entry.duration,
						entry.cost,
						entry.comments,
						task_name,
						project_name,
						client_name,
						username
					])
				# All other cases with task assigned.
				elif entry.client and entry.client.id == client:

					client_name = entry.client.name

					if entry.task:
						task_name = entry.task.name
					if entry.project:
						project_name = entry.project.name
					if entry.user:
						username = entry.user.username

					total_cost += entry.cost

					table_data.append([
						entry.description,
						entry.starttime,
						entry.endtime,
						entry.duration,
						entry.cost,
						entry.comments,
						task_name,
						project_name,
						client_name,
						username
					])

			# Generates the table with the set data
			table = Table(table_data)
			table.setStyle(TableStyle(
				[
					('BACKGROUND', (0, 0), (9, 0), grey),
					('TEXTCOLOR', (0, 0), (9, 0), white),
					('ALIGN', (0, 0), (-1, -1), 'CENTER'),
					('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
					('INNERGRID', (0, 0), (-1, -1), 0.25, black),
					('BOX', (0, 0), (-1, -1), 0.25, black),
				]
			))

			# Appends the table to the report
			elements.append(table)
			elements.append(Spacer(36, 20))
			elements.append(Paragraph(_('Total cost: %s EUR') % total_cost, styles['Heading2']))
			elements.append(PageBreak())

		# Builds the report
		pdf_report.build(elements)

		# Temporarily stores the report in filesystem in order to assign it to the database
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

		# Returns JSON stating that the report was generated. However, for now, the return string is not used.
		data = {
			'result': 'report_generated',
		}
		return JsonResponse(data)

	def report_entryreportpdf(self, report_type):
		"""
		Generates a report that lists all the entries in a given time interval.
		:param report_type: the requested report type
		:return: JSON with the result
		"""

		# standard distance for report
		margin = 1.5

		# Create the PDF object
		timestamp = int(time.time())
		filename = report_type + str(timestamp)
		pdf_report = SimpleDocTemplate('reports/{0}.pdf'.format(filename), author="Chronos Platform",
		                               rightMargin=margin * cm, leftMargin=margin * cm, topMargin=margin * cm,
		                               bottomMargin=margin * cm, pagesize=landscape(A4))
		# Prepares the filters
		q_objs = self.advanced_filter(self.request)

		# Fetch all filtered entries
		entries = Entry.objects.select_related().filter(*q_objs)

		# Generates the table header
		table_data = [['Description', 'Start time', 'End time', 'Duration (min.)', 'Cost(EUR)', 'Comments', 'Task',
		               'Project', 'Client', 'User']]

		# Variable used to calculate the total cost for the sheet.
		total_cost = Decimal.from_float(0.00)

		# Generates the table data using the fetch data.
		for entry in entries:

			task_name = project_name = client_name = username = ''

			if entry.task:
				task_name = entry.task.name
			if entry.project:
				project_name = entry.project.name
			if entry.client:
				client_name = entry.client.name
			if entry.user:
				username = entry.user.username

			total_cost += entry.cost

			table_data.append([
				entry.description,
				entry.starttime,
				entry.endtime,
				entry.duration,
				entry.cost,
				entry.comments,
				task_name,
				project_name,
				client_name,
				username
			])

		# Appends the table to the report
		table = Table(table_data)
		table.setStyle(TableStyle(
			[
				('BACKGROUND', (0, 0), (9, 0), grey),
				('TEXTCOLOR', (0, 0), (9, 0), white),
				('ALIGN', (0, 0), (-1, -1), 'CENTER'),
				('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
				('INNERGRID', (0, 0), (-1, -1), 0.25, black),
				('BOX', (0, 0), (-1, -1), 0.25, black),
			]
		))

		# Style element used by the report
		styles = getSampleStyleSheet()

		# Report elements list
		elements = []

		# Sets the Header
		elements.append(Paragraph(_('Chronos entries report'), styles['Heading1']))
		elements.append(Spacer(36, 20))
		elements.append(Paragraph(_('Report created using Chronos platform'), styles['Heading2']))
		elements.append(Paragraph(_('Generated on %s') % time.ctime(time.time()), styles['Normal']))
		elements.append(PageBreak())
		elements.append(table)
		elements.append(Spacer(36, 20))
		elements.append(Paragraph(_('Total cost: %s EUR') % total_cost, styles['Heading2']))

		# Build the report
		pdf_report.build(elements)

		# Temporarily stores the report in filesystem in order to assign it to the database
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

		# Returns JSON stating that the report was generated. However, for now, the return string is not used.
		data = {
			'result': 'report_generated',
		}
		return JsonResponse(data)

	def switch(self, report_type):
		"""
		Function that is used to determine the requested report type.
		:param report_type: The requested report type
		:return: the result of the requested report type execution
		"""
		method_name = 'report_' + str(report_type)

		def default():
			# Returns JSON stating that the report does not exist.
			data = {
				'result': 'report_does_not_exist',
			}
			return JsonResponse(data)

		# Get the method from 'self'. Default to a lambda.
		method = getattr(self, method_name, default)

		# Call the method as we return it
		return method(report_type)

	def post(self, request, *args, **kwargs):
		"""
		Post function that is called whenever a report is requested.
		:param request: the request for a report
		:return: The report result
		"""
		report_type = request.POST.get('report_type')
		return self.switch(report_type)


class DownloadReportView(LoginRequiredMixin, TemplateView):
	"""
	View that is used to download the generated reports
	"""

	def post(self, request, *args, **kwargs):
		"""
		Post function that is used to fetch and download the intended report.
		:param request: the form request used to request the download
		:return: HttpResponse object with attachment for download
		"""

		report = Report.objects.get(pk=request.POST.get('pk'))
		fs = FileSystemStorage('/')
		with fs.open(report.file.url) as pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			response['Content-Disposition'] = 'attachment; filename="{0}"'.format(report.name)
			return response
