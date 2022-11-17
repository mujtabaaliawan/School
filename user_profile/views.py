from .models import User
from .serializers import UserSerializer
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from .admin_permission import IsAdmin


class UserList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = [IsAdmin]


class UserUpdate(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = [IsAdmin]