from rest_framework import permissions


class IsDeleteOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return self.only_delete_permission(request)

    def has_object_permission(self, request, view, obj):
        return self.only_delete_permission(request)

    @staticmethod
    def only_delete_permission(request):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.method == 'DELETE'
