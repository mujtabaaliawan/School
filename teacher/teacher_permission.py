from rest_framework.permissions import BasePermission
from .models import Teacher


class IsTeacher(BasePermission):

    def has_permission(self, request, view):
        user_id = request.user.id
        teacher_user_id = Teacher.objects.get(id=view.kwargs['pk']).user.id
        if user_id is None:
            return False
        return user_id == teacher_user_id or request.user.is_superuser
