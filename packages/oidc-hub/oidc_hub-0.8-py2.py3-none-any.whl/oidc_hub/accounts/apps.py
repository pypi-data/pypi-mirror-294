from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class AccountsConfig(AppConfig):
    name = "oidc_hub.accounts"
    label = "accounts"
    verbose_name = _("Identities and Accesses")
