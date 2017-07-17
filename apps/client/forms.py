from django.forms import ModelForm

from apps.client.models import TClient


class ClientForm(ModelForm):
    class Meta:
        model = TClient
        fields = ['name', 'description', 'comments', 'vat', 'street', 'postal_code', 'city', 'country',
                  'contact_person', 'email', 'phone', 'mobile', 'website', 'is_visible']