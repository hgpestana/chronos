from django.forms import ModelForm

from apps.client.models import TClient


class ClientForm(ModelForm):
    """
    Client form used to add or update a client in the Chronos platform.
    TODO: Develop this form
    """
    class Meta:
        model = TClient
        fields = ['name', 'description', 'comments', 'vat', 'street', 'postal_code', 'city', 'country',
                  'contact_person', 'email', 'phone', 'mobile', 'website', 'is_visible']