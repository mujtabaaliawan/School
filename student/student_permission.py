from rest_framework.permissions import BasePermission
from student.models import Student


class IsStudent(BasePermission):

    def has_permission(self, request, view):
        user_id = request.user.id
        student_user_id = Student.objects.get(id=view.kwargs['pk']).user.id
        return user_id == student_user_id or request.user.is_superuser


class IsStudentAdmin(BasePermission):

    def has_permission(self, request, view):
        user_id = request.user.id
        student_user_id = Student.objects.get(id=view.kwargs['pk']).user.id
        return user_id == student_user_id or request.user.is_admin or request.user.is_superuser


