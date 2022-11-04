from rest_framework.permissions import BasePermission
from teacher.models import Teacher


class TeacherPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        user_profile_id = request.data.get('user_id')
        user_profile = Teacher.objects.get(id=user_profile_id)
        return user_profile.role == 'teacher'
