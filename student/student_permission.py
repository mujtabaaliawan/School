from rest_framework.permissions import BasePermission
from student.models import Student


class IsStudent(BasePermission):

    def has_permission(self, request, view):
        user_id = request.user.id
        student_user_id = Student.objects.get(id=view.kwargs['pk']).user.id
        if user_id is None:
            return False
        return int(user_id) == int(student_user_id)
