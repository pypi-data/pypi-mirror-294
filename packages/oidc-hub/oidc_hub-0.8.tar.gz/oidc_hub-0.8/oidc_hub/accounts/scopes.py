from django.utils.translation import gettext_lazy as _
from oidc_provider.lib.claims import ScopeClaims

class CustomScopeClaims(ScopeClaims):

    info_groups = (
        _(u'Groups'),
        _(u'Access to group memberships'), # Accès à vos adhésions
    )

    def scope_groups(self):
        # self.user - Django user instance.
        # self.userinfo - Dict returned by OIDC_USERINFO function.
        # self.scopes - List of scopes requested.
        # self.client - Client requesting this claims.
        return {
            'groups': ["admin"] if self.user.is_superuser else []
        }
