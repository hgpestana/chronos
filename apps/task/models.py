from django.db import models
from django.utils.translation import ugettext_lazy as _

class TTask (models.Model):
    """
    Task table to be used by the Chronos platform.
    TODO: Develop this table
    """
    name = models.CharField(_('Name'), max_length=255)
    description = models.TextField(_('Description'), blank=True)
    comments = models.TextField(_('Comments'), blank=True)
    price = models.DecimalField(_('Price'), blank=True, null=True, default=0, max_digits=4, decimal_places=2)
    parenttask = models.ForeignKey('self', on_delete=models.SET_NULL, db_column=_('Parent task'), blank=True, null=True)
    is_visible = models.BooleanField(_('Is Visible'))

    class Meta:

        # Translators: This string is used to identify the TClient table name
        verbose_name = _('Task')

        # Translators: This string is used to identify the TClient table name in plural form
        verbose_name_plural = _('Tasks')