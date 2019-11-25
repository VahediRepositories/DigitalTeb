from django.contrib import messages
from django.contrib.auth import mixins
from django.core.exceptions import PermissionDenied


class LoginRequiredMixin(mixins.LoginRequiredMixin):
    def handle_no_permission(self):
        messages.warning(
            self.request,
            'براى دسترسى ، ابتدا بايد وارد حساب كاربرى خود شويد.',
            extra_tags='login-required-warning'
        )
        return super().handle_no_permission()


class AuthenticatedForbiddenMixin:
    def forbid_authenticated(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied
