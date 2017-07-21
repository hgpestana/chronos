from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from apps.project.models import Project
from apps.client.models import Client
from apps.task.models import Task

class Entry (models.Model):
    """
    Entry table to be used by the Chronos platform.
    TODO: Develop this table
    """
    description = models.TextField(_('Description'))
    starttime = models.DateTimeField(_('Start date / time'))
    endtime = models.DateTimeField(_('End date / time'))
    duration = models.IntegerField(_('Duration'))
    comments = models.TextField(_('Comments'))
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, db_column='Project', blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, db_column='Client', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, db_column='User', blank=True, null=True)
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, db_column='Task', blank=True, null=True)

    class Meta:

        # Translators: This string is used to identify the Account table name
        verbose_name = _('Entry')

        # Translators: This string is used to identify the Account table name in plural form
        verbose_name_plural = _('Entries')
