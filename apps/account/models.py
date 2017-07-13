from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class TUser (models.Model):
    """
    User table to be used by the timsheet platform. Adds an additional field to the already defined fields
    in the django auth User table.
    TODO: Develop this table
    """
    description = models.CharField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:

        # Translators: This string is used to identify the TUser table name
        verbose_name = _('User')

        # Translators: This string is used to identify the TUser table name in plural form
        verbose_name_plural = _('Users')
