from oidc_hub import admin
from django.urls import path, include

urlpatterns = [
    path("", include("oidc_hub.accounts.urls", namespace="accounts")),
    path("openid/", include("oidc_provider.urls", namespace="oidc_provider")),
    path("", admin.site.urls),
]
