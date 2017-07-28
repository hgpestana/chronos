from django.forms import ModelForm, ModelChoiceField
from django.utils.translation import ugettext_lazy as _

from apps.task.models import Task


class FormChoiceField(ModelChoiceField):
	def label_from_instance(self, obj):
		return obj.name


class TaskForm(ModelForm):
	"""
	Task form used to add or update a task in the Chronos platform.
	TODO: Develop this form
	"""

	parenttask = FormChoiceField(
		queryset=Task.objects.all().order_by('name'),
		empty_label=_('Please select an option'),
		required=False,
	)

	class Meta:
		model = Task
		fields = ['name', 'description', 'comments', 'price', 'parenttask', 'is_visible']

