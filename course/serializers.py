from .models import Course
from rest_framework import serializers
from teacher.serializers import TeacherSerializer
from teacher.models import Teacher


class CourseSerializer(serializers.ModelSerializer):

    course_teacher = TeacherSerializer(read_only=True)
    course_teacher_id = serializers.PrimaryKeyRelatedField(
        queryset=Teacher.objects.all(), source='course_teacher', write_only=True)

    class Meta:
        model = Course
        fields = '__all__'

