from .models import Student
from .serializers import StudentSerializer, EnrollmentSerializer
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.generics import RetrieveUpdateAPIView
from .student_permission import IsStudent, IsStudentAdmin
from .admin_permission import IsAdmin


class StudentList(ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    permission_classes = [IsAdmin]


class StudentCreate(CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    permission_classes = [IsAdmin]


class StudentUpdate(RetrieveUpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    permission_classes = [IsStudent]


class EnrollmentUpdate(UpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = EnrollmentSerializer

    permission_classes = [IsStudentAdmin]

