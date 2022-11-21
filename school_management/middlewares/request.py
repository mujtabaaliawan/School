from django.utils.deprecation import MiddlewareMixin
from httpie import status
from rest_framework import exceptions


class RequestRoleMiddleware(MiddlewareMixin):


    def process_request(self, request):

        if request.user.id is not None:
            request.teacher = None
            request.student = None
            request.staff = None
            if request.user.is_teacher:
                request.teacher = request.user
            elif request.user.is_student:
                request.student = request.user
            elif request.user.is_admin:
                request.staff = request.user
        return request

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request = self.process_request(request)
        response = self.get_response(request)
        return response
