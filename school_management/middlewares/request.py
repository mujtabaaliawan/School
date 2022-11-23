from django.utils.deprecation import MiddlewareMixin
from teacher.models import Teacher
from staff.models import Staff
from student.models import Student


class RequestRoleMiddleware(MiddlewareMixin):


    def process_request(self, request):

        if request.user.id is not None:
            request.teacher = None
            request.student = None
            request.staff = None
            if request.user.is_student:
                request.student = Student.objects.get(user_id=request.user.id)
            elif request.user.is_teacher:
                request.teacher = Teacher.objects.get(user_id=request.user.id)
            elif request.user.is_admin:
                request.staff = Staff.objects.get(user_id=request.user.id)
        return request

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request = self.process_request(request)
        response = self.get_response(request)
        return response
