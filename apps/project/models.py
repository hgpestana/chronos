from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _


class Project(models.Model):
	"""
	Project table to be used by the Chronos platform.
	TODO: Develop this table
	"""

	name = models.CharField(_('Name'), max_length=255)
	description = models.TextField(_('Description'), blank=True, null=True)
	comments = models.TextField(_('Comments'), blank=True, null=True)
	created = models.DateTimeField(_('Created'), default=now, blank=True, null=True)
	last_updated = models.DateTimeField(_('Last Updated'), default=now, blank=True, null=True)
	is_visible = models.BooleanField(_('Is Visible'))

	class Meta:
		# Translators: This string is used to identify the Client table name
		verbose_name = _('Project')

		# Translators: This string is used to identify the Client table name in plural form
		verbose_name_plural = _('Projects')
