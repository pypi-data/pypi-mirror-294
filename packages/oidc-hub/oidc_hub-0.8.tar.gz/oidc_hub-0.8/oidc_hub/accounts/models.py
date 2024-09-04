from django.contrib.auth.models import AbstractUser, Group as DjangoGroup, Permission
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import UserManager as _UserManager

# Create your models here.

class UserManager(_UserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(username, email, password, **extra_fields)

class User(AbstractUser):
  email = models.EmailField(_("email address"), blank=False, null=False, unique=True)
  is_staff = None
  USERNAME_FIELD = "email"
  REQUIRED_FIELDS = ["username"]

  objects = UserManager()

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
