from .models import Student
from .serializers import StudentSerializer, EnrollmentSerializer, EnrollmentAdminSerializer
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAdminUser
from .student_permission import IsStudentStaff, IsStudent


class StudentList(ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    permission_classes = [IsAdminUser]


class StudentCreate(CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    permission_classes = [IsAdminUser]


class StudentUpdate(RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    permission_classes = [IsStudentStaff]


class EnrollmentNew(UpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = EnrollmentSerializer

    permission_classes = [IsStudent]


class EnrollmentUpdate(RetrieveUpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = EnrollmentAdminSerializer

    permission_classes = [IsAdminUser]