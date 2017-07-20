from django.forms import ModelForm, ModelChoiceField
from django.utils.translation import ugettext_lazy as _

from apps.task.models import TTask


class FormChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class TaskForm(ModelForm):
    """
    Task form used to add or update a task in the Chronos platform.
    TODO: Develop this form
    """

    class Meta:
        model = TTask
        fields = ['name', 'description', 'comments', 'price', 'parenttask', 'is_visible']

    parenttask = FormChoiceField(queryset=TTask.objects.all().order_by('name'),
                                 empty_label=_('Please select an option'), required=False,)
