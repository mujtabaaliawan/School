from rest_framework.permissions import BasePermission
from .models import Result


class IsTeacher(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_teacher


class IsSubjectTeacher(BasePermission):

    def has_permission(self, request, view):
        user_id = request.user.id
        if user_id is None:
            return False
        pk = view.kwargs['pk']
        subject_teacher_id = Result.objects.get(id=pk).course.course_teacher.user.id
        return user_id == subject_teacher_id or request.user.is_superuser

