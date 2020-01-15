from ..permissions import *
from .models import WorkPlace


class IsPlaceStaffOrReadOnly(IsSpecialistOrReadOnly):

    def has_object_permission(self, request, view, obj):
        if super().has_object_permission(request, view, obj):
            if request.method in permissions.SAFE_METHODS:
                return True
            elif isinstance(obj, WorkPlace):
                return obj.has_staff(request.user)
            else:
                return obj.place.has_staff(request.user)
        else:
            return False
