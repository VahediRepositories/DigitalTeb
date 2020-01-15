from django.core.exceptions import PermissionDenied

from ..mixins import NonSpecialistForbiddenMixin


class NonStaffForbiddenMixin(NonSpecialistForbiddenMixin):
    def forbid_non_staff(self, work_place):
        self.forbid_non_specialist()
        if not work_place.has_staff(self.request.user):
            raise PermissionDenied
