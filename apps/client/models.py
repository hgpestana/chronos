from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _


class TClient (models.Model):
    """
    Client table to be used by the Chronos platform.
    TODO: Develop this table
    """
    name = models.CharField(_('Name'), max_length=255)
    description = models.TextField(_('Description'), blank=True)
    comments = models.TextField(_('Comments'), blank=True)
    vat = models.CharField(_('VAT'), max_length=15, blank=True)
    street = models.CharField(_('Street Address'), max_length=255, blank=True)
    postal_code = models.CharField(_('Postal Code'), max_length=15, blank=True)
    city = models.CharField(_('City'), max_length=50, blank=True)
    country = models.CharField(_('Country'), max_length=50, blank=True)
    contact_person = models.CharField(_('Contact Person'), max_length=255, blank=True)
    email = models.CharField(_('Email'), max_length=50, blank=True)
    phone = models.CharField(_('Phone'), max_length=50, blank=True)
    mobile = models.CharField(_('Mobile'), max_length=50, blank=True)
    website = models.CharField(_('Website'), max_length=50, blank=True)
    last_updated = models.DateTimeField(_('Last Updated'), default=now, blank=True)
    is_visible = models.BooleanField(_('Is Visible'))

    class Meta:

        # Translators: This string is used to identify the TClient table name
        verbose_name = _('Client')

        # Translators: This string is used to identify the TClient table name in plural form
        verbose_name_plural = _('Clients')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('view', kwargs={'pk': self.pk})