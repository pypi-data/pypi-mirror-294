from .sites import AdminSite
from django.utils.module_loading import autodiscover_modules

site = AdminSite(name="oidc_hub")

def autodiscover():
    autodiscover_modules("oidc_hub_admin", register_to=site)
