from django.contrib.admin import apps

class AdminConfig(apps.AdminConfig):
    default_auto_field = "django.db.models.BigAutoField"
    default_site = "oidc_hub.admin.AdminSite"
    name = "oidc_hub.admin"
    label = "oidc_hub_admin"