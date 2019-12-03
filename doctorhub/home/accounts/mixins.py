from django.contrib import messages
from django.contrib.auth import mixins
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.utils import translation


class LoginRequiredMixin(mixins.LoginRequiredMixin):
    def handle_no_permission(self):
        messages.warning(
            self.request,
            translation.gettext('You need to login first.'),
            extra_tags='login-required-warning'
        )
        return super().handle_no_permission()

    def get_login_url(self):
        return reverse('login')


class AuthenticatedForbiddenMixin:
    def forbid_authenticated(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied
