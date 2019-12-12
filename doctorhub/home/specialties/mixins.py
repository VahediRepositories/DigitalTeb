from django.core.exceptions import PermissionDenied

from ..modules import specialties


class NonSpecialistForbiddenMixin:
    def forbid_non_specialist(self):
        if not specialties.is_specialist(self.request.user):
            raise PermissionDenied
