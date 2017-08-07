from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _


class Account(models.Model):
	"""
	User table to be used by the Chronos platform. Adds an additional field to the already defined fields
	in the django auth User table.
	TODO: Develop this table
	"""

	user = models.OneToOneField(User, db_column='User', on_delete=models.CASCADE)
	description = models.TextField('Description', blank=True, null=True)
	created = models.DateTimeField('Created', default=now, blank=True, null=True)
	last_updated = models.DateTimeField('Last Updated', default=now, blank=True, null=True)

	class Meta:
		# Translators: This string is used to identify the Account table name
		verbose_name = _('Account')

		# Translators: This string is used to identify the Account table name in plural form
		verbose_name_plural = _('Accounts')