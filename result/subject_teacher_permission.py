from rest_framework.permissions import BasePermission
from course.models import Course


class SubjectTeacherPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        course_id = request.data.get('course')
        course_profile = Course.objects.get(id=course_id)
        assigned_teacher = course_profile.teacher_profile.id
        current_teacher = request.data.get('user_id')
        return int(current_teacher) == int(assigned_teacher)
