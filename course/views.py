from .models import Course
from .serializers import CourseSerializer
from rest_framework.generics import ListCreateAPIView
from course.teacher_permission import TeacherPermission


class CourseViewSet(ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    permission_classes = [TeacherPermission]
