from rest_framework import permissions

from ..modules.specialties import specialties


class IsSpecialistOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user and specialties.is_specialist(request.user)
        )

