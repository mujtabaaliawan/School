from result.models import Result
from result.serializers import ResultSerializer
from rest_framework.generics import ListCreateAPIView
from result.subject_teacher_permission import SubjectTeacherPermission


class ResultViewSet(ListCreateAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer

    permission_classes = [SubjectTeacherPermission]
