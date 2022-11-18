from rest_framework.permissions import BasePermission
from .models import Result


class IsTeacher(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_teacher


class IsSubjectTeacher(BasePermission):

    def has_permission(self, request, view):
        pk = view.kwargs['pk']
        subject_teacher_id = Result.objects.get(id=pk).course.course_teacher.user.id
        user_id = request.user.id
        if user_id is None:
            return False
        return int(user_id) == int(subject_teacher_id) or request.user.is_superuser

