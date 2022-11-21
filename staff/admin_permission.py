from rest_framework.permissions import BasePermission
from .models import Admin


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_admin or request.user.is_superuser


class IsAdminHimself(BasePermission):

    def has_permission(self, request, view):
        user_id = request.user.id
        admin_user_id = Admin.objects.get(id=view.kwargs['pk']).user.id
        return user_id == admin_user_id or request.user.is_superuser
