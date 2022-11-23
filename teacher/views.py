from .models import Teacher
from .serializers import TeacherSerializer
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .admin_permission import IsAdmin
from .teacher_permission import IsTeacher


class TeacherList(ListAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    permission_classes = [IsAuthenticated]


class TeacherCreate(CreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    permission_classes = [IsAdmin]


class TeacherRetrieveUpdate(RetrieveUpdateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    permission_classes = [IsTeacher]

