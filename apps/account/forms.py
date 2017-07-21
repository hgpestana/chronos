from django.forms import ModelForm, CharField, PasswordInput, ValidationError, HiddenInput
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.forms import inlineformset_factory

from apps.account.models import Account


class AccountForm(ModelForm):
    """
    Account form used to add or update an account in the Chronos platform.
    TODO: Develop this form
    """
    class Meta:
        model = Account
        fields = ['description']


class UserForm(ModelForm):
    """
    User form used to add or update a user in the Chronos platform.
    TODO: Develop this form
    """

    password = CharField(widget=PasswordInput(), required=False)
    password_repeat = CharField(widget=PasswordInput(), required=False,)
    is_new_account = CharField(widget=HiddenInput(), required=False,)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_staff', 'is_superuser', 'is_active']

    def clean(self):
        cleaned_data = super(UserForm, self).clean()

        password = cleaned_data.get('password')
        password_repeat = cleaned_data.get('password_repeat')
        is_new_account = cleaned_data.get('is_new_account')

        if is_new_account:
            if not password:
                raise ValidationError(_("You must set a password for this account."), code='no password')

        if password or password_repeat:
            if password != password_repeat:
                raise ValidationError(_("The two password fields must match."), code='different_passwords')
            validate_password(password)

        return cleaned_data

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
