from .models import Teacher
from rest_framework import serializers
from user_profile.serializers import UserSerializer


class TeacherSerializer(serializers.ModelSerializer):
    base_profile = UserSerializer(required=True)

    class Meta:

        model = Teacher
        fields = ['base_profile', 'role']

    def create(self, validated_data):
        user_data = validated_data.get('base_profile')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        teacher, created = Teacher.objects.update_or_create(base_profile=user, role=validated_data.get('role'))
        return teacher
