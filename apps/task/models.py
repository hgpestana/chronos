from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _


class Task(models.Model):
	"""
	Task table to be used by the Chronos platform.
	TODO: Develop this table
	"""

	name = models.CharField('Name', max_length=255)
	description = models.TextField('Description', blank=True, null=True)
	comments = models.TextField('Comments', blank=True, null=True)
	price = models.DecimalField('Price', blank=True, null=True, default=0, max_digits=8, decimal_places=2)
	parenttask = models.ForeignKey('self', on_delete=models.SET_NULL, db_column='Parent task', blank=True, null=True)
	created = models.DateTimeField('Created', default=now, blank=True, null=True)
	last_updated = models.DateTimeField('Last Updated', default=now, blank=True, null=True)
	is_visible = models.BooleanField('Is Visible')

	class Meta:
		# Translators: This string is used to identify the Client table name
		verbose_name = _('Task')

		# Translators: This string is used to identify the Client table name in plural form
		verbose_name_plural = _('Tasks')
