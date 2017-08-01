from django.forms import ModelForm, ModelChoiceField, HiddenInput, CharField
from django.utils.translation import ugettext_lazy as _

from apps.client.models import Client
from apps.entry.models import Entry
from apps.project.models import Project
from apps.task.models import Task


class FormChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class EntryForm(ModelForm):
    """
    Entry form used to add or update an entry in the Chronos platform.
    TODO: Develop this form
    """

    task = FormChoiceField(
        queryset=Task.objects.all().order_by('name'),
        empty_label=_('Please select an option'),
        required=False,
    )

    project = FormChoiceField(
        queryset=Project.objects.all().order_by('name'),
        empty_label=_('Please select an option'),
        required=False,
    )

    client = FormChoiceField(
        queryset=Client.objects.all().order_by('name'),
        empty_label=_('Please select an option'),
        required=False,
    )

    class Meta:
        model = Entry
        fields = ['description', 'starttime', 'endtime', 'comments', 'duration', 'client', 'project', 'task']
