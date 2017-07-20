from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver


class TUser (models.Model):
    """
    User table to be used by the Chronos platform. Adds an additional field to the already defined fields
    in the django auth User table.
    TODO: Develop this table
    """
    description = models.TextField(_('Description'), blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:

        # Translators: This string is used to identify the TUser table name
        verbose_name = _('User')

        # Translators: This string is used to identify the TUser table name in plural form
        verbose_name_plural = _('Users')


@receiver(post_save, sender=User)
def create_user_tuser(sender, instance, created, **kwargs):
    if created:
        TUser.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_tuser(sender, instance, **kwargs):
    instance.tuser.save()