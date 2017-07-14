from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.project.models import TProject
from apps.client.models import TClient
from apps.account.models import TUser
from apps.task.models import TTask

class TEntry (models.Model):
    """
    Entry table to be used by the Chronos platform.
    TODO: Develop this table
    """
    description = models.TextField(_('Description'))
    starttime = models.DateTimeField(_('Start date / time'))
    endtime = models.DateTimeField(_('End date / time'))
    duration = models.IntegerField(_('Duration'))
    comments = models.TextField(_('Comments'))
    project = models.ForeignKey(TProject, on_delete=models.CASCADE, db_column=_('Project'))
    client = models.ForeignKey(TClient, on_delete=models.CASCADE, db_column=_('Client'))
    user = models.ForeignKey(TUser, on_delete=models.CASCADE, db_column=_('User'))
    task = models.ForeignKey(TTask, on_delete=models.CASCADE, db_column=_('Task'))

    class Meta:

        # Translators: This string is used to identify the TUser table name
        verbose_name = _('Entry')

        # Translators: This string is used to identify the TUser table name in plural form
        verbose_name_plural = _('Entries')
