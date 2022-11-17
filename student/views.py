from .models import Student
from .serializers import StudentSerializer, EnrollmentSerializer, EnrollmentAdminSerializer
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.generics import RetrieveUpdateAPIView
from .student_permission import IsStudent
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


class EnrollmentNew(UpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = EnrollmentSerializer

    permission_classes = [IsStudent]


class EnrollmentUpdate(RetrieveUpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = EnrollmentAdminSerializer

    permission_classes = [IsAdmin]
