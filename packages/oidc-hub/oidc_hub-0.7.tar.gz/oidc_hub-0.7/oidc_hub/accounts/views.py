from . import models
from django.contrib.auth import login, get_user_model
from django.contrib.auth import views
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views import generic
from oidc_hub import admin

# Create your views here.

class SiteContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "site_title": admin.site.site_title,
            "site_header": admin.site.site_header
        })
        return context

class PasswordResetView(views.PasswordResetView):
    success_url = reverse_lazy("accounts:pass_reset_done")
    template_name = "accounts/pass/reset.j2"
    email_template_name = "accounts/pass/reset_email.j2"

class PasswordResetDoneView(views.PasswordResetDoneView):
    template_name = "accounts/pass/reset_done.j2"


class PasswordResetConfirmView(views.PasswordResetConfirmView):
    post_reset_login = True
    reset_url_token = "confirm"
    success_url = reverse_lazy("admin:index")

class SignUpView(generic.CreateView):
    model = get_user_model()
    fields = ("username", "password")
    template_name = "accounts/signup.j2"
    success_url = "/"

    def get(self, request, *args, **kwargs):
        self.object = None
        return self.render_to_response(self.get_context_data(token=request.GET.get("token")))

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            if token := request.GET.get("token", None):
                invitation = get_object_or_404(models.Invitation, token=token)
                form.instance.email = invitation.recipient_email
                # turn plain-text password into a hash for database storage
                form.instance.set_password(form.instance.password)
                self.object = form.save()
                invitation.delete()
                login(self.request, self.object)
                return redirect(self.get_success_url())
            else:
                return HttpResponseBadRequest(_("Invalid invitation token."))
        else:
            return self.form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        """
        Redirect any authenticated user to the dashboard.
        """
        if request.user.is_authenticated:
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)
