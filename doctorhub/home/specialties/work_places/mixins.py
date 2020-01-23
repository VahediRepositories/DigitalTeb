from django.core.exceptions import PermissionDenied

from ..mixins import NonSpecialistForbiddenMixin


class NonStaffForbiddenMixin(NonSpecialistForbiddenMixin):
    def forbid_non_staff(self, work_place):
        self.forbid_non_specialist()
        if not work_place.has_staff(self.request.user):
            print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@44444')
            raise PermissionDenied


class NonPlaceOwnerForbiddenMixin(NonStaffForbiddenMixin):
    def forbid_non_owner(self, place):
        self.forbid_non_staff(place)
        if place.owner != self.request.user:
            raise PermissionDenied
