from rest_framework.permissions import BasePermission
from .models import Teacher


class IsTeacher(BasePermission):

    def has_permission(self, request, view):
        if request.teacher is None:
            return False
        teacher_user_id = view.kwargs['pk']
        return request.teacher.id == teacher_user_id or request.user.is_superuser
