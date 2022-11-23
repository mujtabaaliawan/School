from .models import Staff
from rest_framework import serializers
from user_profile.serializers import UserSerializer


class StaffSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Staff
        fields = ['id', 'user', 'role', 'mobile_number']

    def create(self, validated_data):
        user = UserSerializer.create(self, validated_data=validated_data)
        role = validated_data.get('role')
        mobile_number = validated_data.get('mobile_number')
        staff, created = Staff.objects.update_or_create(user=user, role=role, mobile_number=mobile_number)
        return staff
