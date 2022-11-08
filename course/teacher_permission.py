from rest_framework.permissions import BasePermission
from teacher.models import Teacher


class TeacherPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        profile_id = request.data.get('user_id')
        profile = Teacher.objects.get(id=profile_id)
        return profile.role == 'teacher'
