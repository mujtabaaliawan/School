from result.models import Result
from result.serializers import ResultSerializer, ResultListSerializer
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from .result_permission import IsTeacher, IsSubjectTeacher
from .admin_permission import IsAdmin


class ResultList(ListAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultListSerializer

    permission_classes = [IsAdmin]


class ResultCreate(CreateAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer

    permission_classes = [IsTeacher]


class ResultUpdate(RetrieveUpdateDestroyAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer

    permission_classes = [IsSubjectTeacher]
