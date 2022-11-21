from .models import Staff
from .serializers import StaffSerializer
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .admin_permission import IsAdmin, IsAdminHimself


class StaffList(ListAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer

    permission_classes = [IsAuthenticated]


class StaffCreate(CreateAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer

    permission_classes = [IsAdmin]


class StaffUpdate(RetrieveUpdateAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer

    permission_classes = [IsAdminHimself]

