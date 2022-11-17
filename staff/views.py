from .models import Admin
from .serializers import StaffSerializer
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .admin_permission import IsAdmin


class AdminList(ListAPIView):
    queryset = Admin.objects.all()
    serializer_class = StaffSerializer

    permission_classes = [IsAuthenticated]


class AdminCreate(CreateAPIView):
    queryset = Admin.objects.all()
    serializer_class = StaffSerializer

    permission_classes = [IsAdmin]


class AdminUpdate(RetrieveUpdateAPIView):
    queryset = Admin.objects.all()
    serializer_class = StaffSerializer

    permission_classes = [IsAdmin]

