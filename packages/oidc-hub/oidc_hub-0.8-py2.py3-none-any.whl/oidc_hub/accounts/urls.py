from . import views
from django.urls import re_path
from oidc_hub.admin import site

app_name = "accounts"

extra_context = {
    "site_title": site.site_title,
    "site_header": site.site_header
}

urlpatterns = [
    # registration
    re_path(r"signup/?", views.SignUpView.as_view(extra_context=extra_context), name="signup"),
    # reset password
    re_path(r"pass/reset/?$", views.PasswordResetView.as_view(extra_context=extra_context), name="pass_reset"),
    re_path(r"pass/reset/sent/?$", views.PasswordResetDoneView.as_view(extra_context=extra_context), name="pass_reset_done"),
    re_path(r"pass/reset/(?P<uidb64>[^.]*)/(?P<token>[^.]*)/?$", views.PasswordResetConfirmView.as_view(extra_context=extra_context), name="pass_reset_confirm"),
]
