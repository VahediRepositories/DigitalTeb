from rest_framework import permissions

from ..modules import specialties


class IsSpecialistOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return specialties.is_specialist(request.user)
