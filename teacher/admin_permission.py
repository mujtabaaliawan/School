from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        if request.user.id is None:
            return False
        return request.user.is_admin or request.user.is_superuser
