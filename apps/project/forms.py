from django.forms import ModelForm

from apps.project.models import Project


class ProjectForm(ModelForm):
	"""
	Project form used to add or update a project in the Chronos platform.
	TODO: Develop this form
	"""

	class Meta:
		model = Project
		fields = ['name', 'description', 'comments', 'is_visible']
