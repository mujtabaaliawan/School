from .models import Student
from .serializers import StudentSerializer, StudentCourseSerializer
from rest_framework.generics import ListCreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny


class StudentViewSet(ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    permission_classes = [AllowAny]


class EnrollCourseViewSet(UpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentCourseSerializer
