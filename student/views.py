from .models import Student
from .serializers import StudentSerializer, StudentCourseSerializer
from rest_framework.generics import ListCreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.authentication import BasicAuthentication


class StudentViewSet(ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    authentication_classes = [BasicAuthentication]
    permission_classes = [AllowAny]


class EnrollCourseViewSet(UpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentCourseSerializer
