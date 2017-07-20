from django.forms import ModelForm
from django.contrib.auth.models import User
from django.forms import inlineformset_factory

from apps.account.models import TUser


class AccountForm(ModelForm):
    """
    Account form used to add or update an account in the Chronos platform.
    TODO: Develop this form
    """
    class Meta:
        model = TUser
        fields = ['description']


class UserForm(ModelForm):
    """
    User form used to add or update a user in the Chronos platform.
    TODO: Develop this form
    """
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'is_staff', 'is_superuser', 'is_active']

AccountInlineFormSet = inlineformset_factory(User, TUser, form=AccountForm, extra=1, can_delete=True)
