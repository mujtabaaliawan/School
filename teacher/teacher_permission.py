from rest_framework.permissions import BasePermission
from .models import Teacher


class IsTeacherStaff(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':
            user_id = request.user.id
            teacher_user_id = Teacher.objects.get(user_id=user_id).user.id
            return int(user_id) == int(teacher_user_id) or request.user.is_staff
        else:
            return request.user.is_staff