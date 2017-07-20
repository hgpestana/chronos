from django.forms import ModelForm

from apps.project.models import TProject


class ProjectForm(ModelForm):
    """
    Project form used to add or update a project in the Chronos platform.
    TODO: Develop this form
    """
    class Meta:
        model = TProject
        fields = ['name', 'description', 'comments', 'is_visible']