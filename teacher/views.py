from .models import Teacher
from .serializers import TeacherSerializer, TeacherBasicSerializer
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .teacher_permission import IsTeacherStaff


class TeacherDetailList(ListAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    permission_classes = [IsAdminUser]


class TeacherList(ListAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherBasicSerializer

    permission_classes = [IsAuthenticated]


class TeacherCreate(CreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    permission_classes = [IsAdminUser]


class TeacherUpdate(RetrieveUpdateDestroyAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    permission_classes = [IsTeacherStaff]
