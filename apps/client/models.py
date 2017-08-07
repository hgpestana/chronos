from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _


class Client(models.Model):
	"""
	Client table to be used by the Chronos platform.
	TODO: Develop this table
	"""

	name = models.CharField('Name', max_length=255)
	description = models.TextField('Description', blank=True, null=True)
	comments = models.TextField('Comments', blank=True, null=True)
	vat = models.CharField('VAT', max_length=15, blank=True, null=True)
	street = models.CharField('Street Address', max_length=255, blank=True, null=True)
	postal_code = models.CharField('Postal Code', max_length=15, blank=True, null=True)
	city = models.CharField('City', max_length=50, blank=True, null=True)
	country = models.CharField('Country', max_length=50, blank=True, null=True)
	contact_person = models.CharField('Contact Person', max_length=255, blank=True, null=True)
	email = models.CharField('Email', max_length=50, blank=True, null=True)
	phone = models.CharField('Phone', max_length=50, blank=True, null=True)
	mobile = models.CharField('Mobile', max_length=50, blank=True, null=True)
	website = models.CharField('Website', max_length=50, blank=True, null=True)
	created = models.DateTimeField('Created', default=now, blank=True, null=True)
	last_updated = models.DateTimeField('Last Updated', default=now, blank=True, null=True)
	is_visible = models.BooleanField('Is Visible')

	class Meta:
		# Translators: This string is used to identify the Client table name
		verbose_name = _('Client')

		# Translators: This string is used to identify the Client table name in plural form
		verbose_name_plural = _('Clients')

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('view', kwargs={'pk': self.pk})
