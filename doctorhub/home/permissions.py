from rest_framework import permissions


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsOwnerOrReadOnly(permissions.IsAuthenticatedOrReadOnly):

    def has_object_permission(self, request, view, obj):
        if super().has_object_permission(request, view, obj):
            if request.method in permissions.SAFE_METHODS:
                return True
            else:
                return obj.owner == request.user
        else:
            return False


class IsDelete(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method == 'DELETE'
