from django.conf import settings
from django.contrib import messages
from django.contrib.admin import ModelAdmin, action
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.admin import UserAdmin as _UserAdmin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from oidc_hub import accounts
from oidc_hub.admin import site
from django.contrib.admin.views.main import ChangeList
from django.urls.exceptions import NoReverseMatch

# Register your models here.

class UserChangeList(ChangeList):
  def __init__(self, request, *args, **kwargs):
    super().__init__(request, *args, **kwargs)
    self.request = request
    
  def url_for_result(self, result):
    if any([
      self.request.user.is_superuser,
      not self.request.user.is_superuser and result == self.request.user
    ]):
      return super().url_for_result(result)
    raise NoReverseMatch

class UserAdmin(_UserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "is_superuser", "is_active", "date_joined", "last_login")
    list_filter = ("is_superuser", "is_active", "groups")

    restricted_fields = ['is_superuser', 'user_permissions', 'groups', 'date_joined', 'last_login']
    
    add_fieldsets = (
      (None, {
        "classes": ["wide"], 
        "fields": ["username", "email", "password1", "password2"]
      }),
    )
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (_("Permissions"), {
          "fields": (
            "is_active",
            "is_superuser",
            "groups",
            "user_permissions",
          )
        }),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    def get_fieldsets(self, request, obj=None):
        if not request.user.is_superuser:
            return [
                (title, {"fields": [field for field in fields["fields"] 
                if field not in ("user_permissions",)]})
                for title, fields in self.fieldsets
            ]
        return self.fieldsets

    def get_readonly_fields(self, request, obj=None):
      if not request.user.is_superuser:
        return self.restricted_fields
      return super().get_readonly_fields(request, obj)

    def has_view_permission(self, request, obj=None):
      if not request.user.is_superuser and obj:
        return request.user == obj
      return super().has_view_permission(request, obj)

    def has_change_permission(self, request, obj=None):
      if not request.user.is_superuser:
        return request.user == obj
      return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
      if not request.user.is_superuser and obj:
        return request.user == obj
      return super().has_delete_permission(request, obj)

    def get_changelist(self, request, **kwargs):
      return UserChangeList

    def get_list_display(self, request):
        if not request.user.is_superuser:
          list_display = list(super().get_list_display(request)) # shallow copy
          for field in ('first_name', 'last_name', 'email'):
            try:
              list_display.remove(field)
            except:
              pass
          return list_display
        return self.list_display


@action(description=_("Send selected %(verbose_name_plural)s"))
def send(modeladmin, request, queryset):
  print("send")

class InvitationAdmin(ModelAdmin):
  list_display = ["recipient_email", "created_at"]
  ordering = ["recipient_email"]
  actions = [send]
  signup_url = "/signup"

  def save_model(self, request, obj, form, change):
    """
    Given a model instance save it to the database.
    """
    obj.save()
    self.send_email(request, obj, change)

  def send_email(self, request, obj, change):
    # compute an email subject
    current_site = get_current_site(request)
    subject = _("You're invited to sign up")
    # build up a context object for rendering email content
    context = {
        "external_url": request.build_absolute_uri("/"),
        "registration_link": f"{request.build_absolute_uri(self.signup_url)}?token={obj.token}",
        "site_name": current_site.name,
        "cluster_name": getattr(settings, "CLUSTER_NAME", "")
    }

    # render email alternatives
    html = render_to_string("accounts/emails/invitation.j2", context)
    txt = render_to_string("accounts/emails/invitation.txt", context)

    try:
        # send email to recipient
        email = EmailMultiAlternatives(
            subject, txt, settings.DEFAULT_FROM_EMAIL, [obj.recipient_email]
        )
        email.attach_alternative(html, "text/html")
        email.send()

        messages.success(
            request,
            _("An invitation has been sent to {}").format(obj.recipient_email),
        )
    except Exception as e:
        # email validation errors
        messages.error(
            request,
            str(e)
        )

# Register models
site.register(accounts.models.Group, GroupAdmin)
site.register(get_user_model(), UserAdmin)
site.register(accounts.models.Invitation, InvitationAdmin)

from oidc_provider.models import Client, UserConsent
from oidc_provider.admin import ClientAdmin

site.register(Client, ClientAdmin)
site.register(UserConsent)
