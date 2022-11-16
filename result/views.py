from result.models import Result
from result.serializers import ResultSerializer
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from .result_permission import IsTeacher, IsSubjectTeacher
from rest_framework.permissions import IsAdminUser


class ResultList(ListAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer

    permission_classes = [IsAdminUser]


class ResultCreate(CreateAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer

    permission_classes = [IsTeacher]


class ResultUpdate(RetrieveUpdateDestroyAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer

    permission_classes = [IsSubjectTeacher]
