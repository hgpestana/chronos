from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from apps.client.models import Client
from apps.project.models import Project
from apps.task.models import Task


class Entry(models.Model):
	"""
	Entry table to be used by the Chronos platform.
	TODO: Develop this table
	"""

	description = models.TextField(_('Description'))
	starttime = models.CharField(_('Start date / time'), max_length=20)
	endtime = models.CharField(_('End date / time'), max_length=20)
	duration = models.IntegerField(_('Duration'), blank=True, null=True)
	comments = models.TextField(_('Comments'), blank=True, null=True)
	project = models.ForeignKey(Project, on_delete=models.SET_NULL, db_column='Project', blank=True, null=True)
	client = models.ForeignKey(Client, on_delete=models.SET_NULL, db_column='Client', blank=True, null=True)
	user = models.ForeignKey(User, on_delete=models.SET_NULL, db_column='User', blank=True, null=True)
	task = models.ForeignKey(Task, on_delete=models.SET_NULL, db_column='Task', blank=True, null=True)
	created = models.DateTimeField(_('Created'), default=now, blank=True, null=True)
	last_updated = models.DateTimeField(_('Last Updated'), default=now, blank=True, null=True)

	class Meta:
		# Translators: This string is used to identify the Account table name
		verbose_name = _('Entry')

		# Translators: This string is used to identify the Account table name in plural form
		verbose_name_plural = _('Entries')
