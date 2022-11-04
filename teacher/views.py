from .models import Teacher
from .serializers import TeacherSerializer
from rest_framework.generics import ListCreateAPIView
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import AllowAny


class TeacherViewSet(ListCreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    authentication_classes = [BasicAuthentication]
    permission_classes = [AllowAny]
