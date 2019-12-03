from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.utils import translation


class ConfirmedForbiddenMixin:
    def forbid_confirmed(self):
        phone = self.request.user.profile.phone
        if phone.verified:
            raise PermissionDenied


class CheckPhoneVerifiedMixin:
    @staticmethod
    def check_phone_verified(request):
        if request.user.is_authenticated:
            phone = request.user.profile.phone
            if not phone.verified:
                messages.warning(
                    request,
                    translation.gettext(
                            'Your cell phone number has not been verified. '
                            'In order to have access to all resources, '
                            'you have to verify your number.'
                    ),
                    'phone-not-confirmed-warning'
                )
