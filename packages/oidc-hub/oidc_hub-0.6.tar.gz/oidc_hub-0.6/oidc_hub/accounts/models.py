from django.contrib.auth.models import AbstractUser, Group as DjangoGroup, Permission
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _


# Create your models here.

class User(AbstractUser):
  email = models.EmailField(_("email address"), blank=False, null=False, unique=True)
  is_staff = None
  USERNAME_FIELD = "email"
  REQUIRED_FIELDS = ["username"]

  def save(self, *args, **kwargs):
    adding = self._state.adding
    super().save(*args, **kwargs)
    if adding:
      for codename in ["view_user"]:
        try:
          permission = Permission.objects.get(codename=codename)
          self.user_permissions.add(permission)
        except Permission.DoesNotExist:
          pass

class Group(DjangoGroup):
  class Meta:
    verbose_name = _('group')
    verbose_name_plural = _('groups')
    proxy = True


class Invitation(models.Model):
  recipient_email = models.EmailField(verbose_name=_("Email address"), unique=True)
  token = models.CharField(verbose_name=_("Token"), max_length=32, unique=True, editable=False)
  created_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return self.recipient_email
  
  def save(self, *args, **kwargs):
    adding = self._state.adding
    if adding:
      self.token = get_random_string(length=self._meta.get_field("token").max_length)
    super().save(*args, **kwargs)
