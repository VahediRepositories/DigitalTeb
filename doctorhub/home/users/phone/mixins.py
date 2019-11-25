from django.contrib import messages
from django.core.exceptions import PermissionDenied


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
                    'شماره موبايل شما هنوز فعال نشده است. براى استفاده از تمامى امكانات، بايد شماره ى خود را فعال كنيد.',
                    'phone-not-confirmed-warning'
                )
