from rest_framework import permissions

from ..modules.specialties import specialties


class IsSpecialistOrReadOnly(permissions.IsAuthenticatedOrReadOnly):

    def has_permission(self, request, view):
        if super().has_permission(request, view):
            if request.method in permissions.SAFE_METHODS:
                return True
            elif specialties.is_specialist(request.user):
                return True
            else:
                return False
        else:
            return False


