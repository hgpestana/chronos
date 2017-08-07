import os

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class Report(models.Model):
	"""
	Report table to be used by the Chronos platform.
	TODO: Develop this table
	"""

	name = models.CharField('Name', max_length=255)
	type = models.CharField('Type', max_length=255, blank=True, null=True)
	user = models.ForeignKey(User, on_delete=models.SET_NULL, db_column='User', blank=True, null=True)
	file = models.FileField(upload_to='reports',blank=True, null=True)
	filetype = models.CharField('File type', max_length=255, blank=True, null=True)
	created = models.DateTimeField('Created', default=now, blank=True, null=True)

	class Meta:
		# Translators: This string is used to identify the Report table name
		verbose_name = _('Report')

		# Translators: This string is used to identify the Report table name in plural form
		verbose_name_plural = _('Reports')

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('view', kwargs={'pk': self.pk})


class ReportType(models.Model):
	"""
	Report type table to be used by the Chronos platform.
	TODO: Develop this table
	"""
	code = models.CharField('Code', max_length=255)
	name = models.CharField('Name', max_length=255)
	description = models.TextField('Comments', blank=True, null=True)
	filetype = models.CharField('File type', max_length=255, blank=True, null=True)
	created = models.DateTimeField('Created', default=now, blank=True, null=True)

	class Meta:
		# Translators: This string is used to identify the Report type table name
		verbose_name = _('Report type')

		# Translators: This string is used to identify the Report type table name in plural form
		verbose_name_plural = _('Report types')

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('view', kwargs={'pk': self.pk})