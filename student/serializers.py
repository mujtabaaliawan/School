from .models import Student
from rest_framework import serializers
from userprofile.serializers import UserSerializer


class StudentSerializer(serializers.ModelSerializer):
    base_profile = UserSerializer(required=True)

    class Meta:

        model = Student
        fields = ['id', 'base_profile', 'role', 'enrolled_course']
        extra_kwargs = {
            'password': {'write_only': True},
            'enrolled_course': {'read_only': True}
        }

    def create(self, validated_data):
        user_data = validated_data.pop('base_profile')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        student, created = Student.objects.update_or_create(base_profile=user, role=validated_data.pop('role'))
        return student


class StudentCourseSerializer(serializers.ModelSerializer):

    class Meta:

        model = Student
        fields = ['id', 'enrolled_course']

    def update(self, instance, validated_data):
        course = validated_data.get('enrolled_course')
        instance.enrolled_course.add(course[0])
        return instance
