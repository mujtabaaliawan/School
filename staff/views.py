from .models import Staff
from .serializers import StaffSerializer
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class StaffList(ListAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer

    permission_classes = [IsAuthenticated]


class StaffCreate(CreateAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer

    permission_classes = [IsAdminUser]


class StaffUpdate(RetrieveUpdateDestroyAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer

    permission_classes = [IsAdminUser]

