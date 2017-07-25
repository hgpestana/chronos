from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _


class Account(models.Model):
	"""
	User table to be used by the Chronos platform. Adds an additional field to the already defined fields
	in the django auth User table.
	TODO: Develop this table
	"""

	user = models.OneToOneField(User, db_column='User', on_delete=models.CASCADE)
	description = models.TextField(_('Description'), blank=True, null=True)
	created = models.DateTimeField(_('Created'), default=now, blank=True, null=True)
	last_updated = models.DateTimeField(_('Last Updated'), default=now, blank=True, null=True)

	class Meta:
		# Translators: This string is used to identify the Account table name
		verbose_name = _('Account')

		# Translators: This string is used to identify the Account table name in plural form
		verbose_name_plural = _('Accounts')


@receiver(post_save, sender=User)
def create_user_account(sender, instance, created, **kwargs):
	if created:
		Account.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_account(sender, instance, **kwargs):
	instance.account.save()
