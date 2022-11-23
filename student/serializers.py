from .models import Student
from rest_framework import serializers
from user_profile.serializers import UserSerializer
from course.serializers import CourseSerializer


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    enrolled_course = CourseSerializer(many=True)

    class Meta:

        model = Student
        fields = ['id', 'user', 'role', 'mobile_number', 'enrolled_course']
        extra_kwargs = {
            'enrolled_course': {'read_only': True}
        }

    def create(self, validated_data):
        user = UserSerializer.create(self, validated_data=validated_data)
        role = validated_data.get('role')
        mobile_number = validated_data.get('mobile_number')
        student, created = Student.objects.update_or_create(user=user, role=role, mobile_number=mobile_number)
        return student


class EnrollmentSerializer(serializers.ModelSerializer):

    class Meta:

        model = Student
        fields = ['id', 'enrolled_course']

    def update(self, instance, validated_data):
        request = self.context['request']
        course = validated_data.get('enrolled_course')
        if request.user.is_student:
            if len(course) != 0:
                instance.enrolled_course.add(course[0])
            return instance
        return super().update(instance, validated_data)
