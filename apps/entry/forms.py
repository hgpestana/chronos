from django.forms import ModelForm, ModelChoiceField, DateTimeField, DateTimeInput
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
        queryset=Task.objects.all().filter(is_visible=True).order_by('name'),
        empty_label=_('Please select an option'),
        required=False,
    )

    project = FormChoiceField(
        queryset=Project.objects.all().filter(is_visible=True).order_by('name'),
        empty_label=_('Please select an option'),
        required=False,
    )

    client = FormChoiceField(
        queryset=Client.objects.all().filter(is_visible=True).order_by('name'),
        empty_label=_('Please select an option'),
        required=False,
    )

    starttime = DateTimeField(
        input_formats=['%Y-%m-%d %H:%M'],
        widget=DateTimeInput(format='%Y-%m-%d %H:%M')
    )

    endtime = DateTimeField(
        input_formats=['%Y-%m-%d %H:%M'],
        widget=DateTimeInput(format='%Y-%m-%d %H:%M')
    )

    class Meta:
        model = Entry
        fields = ['description', 'starttime', 'endtime', 'comments', 'duration', 'client', 'project', 'task']
