from .models import Course
from .serializers import CourseSerializer
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class CourseList(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    permission_classes = [IsAuthenticated]


class CourseCreate(CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    permission_classes = [IsAdminUser]


class CourseUpdate(RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    permission_classes = [IsAdminUser]
